import aiosqlite
from datetime import datetime, timezone
from typing_extensions import Literal

default_values = {
    "wallet": 0,
    "bank": 0,
    "win": 0,
    "loss": 0,
    "kd_rate": 0.0,
    "xp": 0,
    "level": 0,
    "daily_cd": "01/01/1970 00:00:00",
    "streak": 1,
    "inventory": "",
    "held_item": "None",
}

class LiveDatabase:
    def __init__(self, dir: str, dbname: str = "hypothermia"):
        self.dir = dir
        self.dbname = dbname
        
    async def setup_database(self):
        """Creates the database, complete with a table. Does not work if the database already exists.
        """
        f = None
        db = None
        try:
            f = open(self.dir + f"{self.dbname}.db", "r+b")
            f.read()
            f.close()
            
            print("LiveDB (SQLite) loaded.")
            return
        except FileNotFoundError:
            pass
        
        try:
            db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
            
            await db.execute("CREATE TABLE users(id INTEGER, wallet INTEGER, bank INTEGER, xp INTEGER, level INTEGER)")
            await db.execute("CREATE TABLE daily(id INTEGER, daily_cd TEXT, streak INTEGER)")
            await db.execute("CREATE TABLE items(id INTEGER, inventory TEXT, held_item TEXT)")
            await db.execute("CREATE TABLE score(id INTEGER, win INTEGER, loss INTEGER, kd_rate REAL)")
            await db.commit()
            
            await db.close()
            print("LiveDB (SQLite) generated.")
        except Exception as e:
            try:
                await db.close()
            except:
                pass
                
            raise Exception(f"LiveDB (SQLite) generation failed: {e}")
            
    async def get_dailycd(self, id):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        now = None
        before = None
        
        try:
            
            dt = await db.execute("SELECT daily_cd FROM daily WHERE id = ?", (id,))
            dt = await dt.fetchall()
            await db.close()
            
            dt = dt[0][0]
            dt = dt.split(" ", 1)
            
            dt[0] = dt[0].split("/")
            dt[1] = dt[1].split(":")

            before = datetime(int(dt[0][2]), int(dt[0][1]), int(dt[0][0]), int(dt[1][0]), int(dt[1][1]), int(dt[1][2]), tzinfo = timezone.utc)
            now = datetime.now(timezone.utc)
            difference = now - before
            
            if difference.days == 0:
                hours = int(24 - difference.seconds / 3600)
                minutes = int(60 - difference.seconds / 60) % 60
                seconds = int(60 - difference.seconds) % 60
            
                return f"{hours}h {minutes}m {seconds}s"
            else:
                return difference.days
        except Exception as e:
            print(e)
            
            try:
                await db.close()
            except:
                pass
    
    async def set_dailycd(self, id):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        now = None
        dt = ""
        
        try:
            
            now = datetime.now(timezone.utc)
            dt = now.strftime("%d/%m/%Y %H:%M:%S")
            
            await db.execute("UPDATE daily SET daily_cd = ? WHERE id = ?", (dt, id))
            await db.commit()
            
            await db.close()
        except Exception as e:
            print(e)
            
            try:
                await db.close()
            except:
                pass
    
    async def get_streak(self, id: int):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        streak = 0
        
        try:
            streak = await db.execute("SELECT streak FROM daily WHERE id = ?", (id,))
            streak = await streak.fetchall()
            
            await db.close()
            return streak[0][0]
        except Exception as e:
            print(e)
            
            try:
                await db.close()
            except:
                pass
    
    async def edit_streak(self, id: int, act: str, amount: int = 1):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        streak = 0
        
        if act in ["set", "add"]:
            try:
                streak = await self.get_streak(id)
                
                if act == "set":
                    await db.execute("UPDATE daily SET streak = ? WHERE id = ?", (amount, id))
                elif act == "add":
                    streak += amount
                    await db.execute("UPDATE daily SET streak = ? WHERE id = ?", (streak, id))
                await db.commit()
                
                await db.close()
                return True
            except Exception as e:
                print(e)
                
                try:
                    await db.close()
                except:
                    pass
        else:
            return False
    
    async def add_user(self, id):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        
        try:
            await db.execute("INSERT INTO users(id, wallet, bank, xp, level) VALUES(?, ?, ?, ?, ?)", (id, default_values["wallet"], default_values["bank"], default_values["xp"], default_values["level"]))
            await db.execute("INSERT INTO items(id, inventory, held_item) VALUES(?, ?, ?)", (id, default_values["inventory"], default_values["held_item"]))
            await db.execute("INSERT INTO daily(id, daily_cd, streak) VALUES(?, ?, ?)", (id, default_values["daily_cd"], default_values["streak"]))
            await db.execute("INSERT INTO score(id, win, loss, kd_rate) VALUES(?, ?, ?, ?)", (id, default_values["win"], default_values["loss"], default_values["kd_rate"]))
            await db.commit()
            
            await db.close()
        except Exception as e:
            print(e)
            try:
                await db.close()
            except:
                pass
            
    async def user_exists(self, id):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        
        try:
            user = await db.execute("SELECT id FROM users WHERE id = ?", (id,))
            user = await user.fetchall()
            await db.close()
            
            if user == []:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            
            try:
                await db.close()
            except:
                pass
            
            return False
            
    async def edit_money(self, id: int, amount: int, dest: str, action: Literal["add", "subtract", "set"]):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        acc = 0
        
        if amount < 0:
            return False
        
        if action in ["add", "subtract", "set"] and dest in ["wallet", "bank"]:
            try:
                retrieved = False
                
                while not retrieved:
                    acc = await self.get_money(id, dest)
                
                    if acc == []:
                        await self.add_user(id)
                    else:
                        retrieved = True
                
                if action == "add":
                    acc += amount
                elif action == "subtract":
                    acc -= amount
                elif action == "set":
                    acc = amount
                    
                if acc < 0:
                    acc = 0
                    
                if dest == "wallet":
                    await db.execute("UPDATE users SET wallet = ? WHERE id = ?", (acc, id))
                elif dest == "bank":
                    await db.execute("UPDATE users SET bank = ? WHERE id = ?", (acc, id))
                await db.commit()
                
                await db.close()
                return True
            except Exception as e:
                print(e)
                
                try:
                    await db.close()
                except:
                    pass
        else:
            return False
        
    async def get_money(self, id: int, dest: str):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        
        try:
            if dest in ["wallet", "bank"]:
                acc = 0
                retrieved = False
                
                while not retrieved:
                    if dest == "wallet":
                        acc = await db.execute("SELECT wallet FROM users WHERE id = ?", (id, ))
                        acc = await acc.fetchall()
                    elif dest == "bank":
                        acc = await db.execute("SELECT bank FROM users WHERE id = ?", (id, ))
                        acc = await acc.fetchall()
                
                    if acc == []:
                        await self.add_user(id)
                    else:
                        acc = acc[0][0]
                        retrieved = True
                
                await db.close()
                return acc
            else:
                return False
        except Exception as e:
            print(e)
                
            try:
                await db.close()
            except:
                pass
            
    async def get_scores(self, id: int):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        val = None
        wl = []
        
        try:
            val = await db.execute("SELECT win FROM score WHERE id = ?", (id, ))
            val = await val.fetchall()
            wl.append(val[0][0])
            
            val = await db.execute("SELECT loss FROM score WHERE id = ?", (id, ))
            val = await val.fetchall()
            wl.append(val[0][0])
            
            val = await db.execute("SELECT kd_rate FROM score WHERE id = ?", (id, ))
            val = await val.fetchall()
            wl.append(val[0][0])
            
            await db.close()
            return wl
        except Exception as e:
            print(e)
                
            try:
                await db.close()
            except:
                pass
            
    async def set_scores(self, id: int, oc: Literal["win", "loss"], score: int = 1):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        wl = await self.get_scores(id)
        wl2 = [wl[0], wl[1]]
        kd = 0
        
        if oc in ["win", "loss"]:
            try:
                if oc == "win":
                    wl2[0] += score
                    
                    if wl2[0] <= 0:
                        wl2[0] = 0
                    
                    kd = wl2[0] / (wl2[0] + wl2[1])
                        
                    await db.execute("UPDATE score SET win = ? WHERE id = ?", (wl2[0], id))
                    await db.execute("UPDATE score SET kd_rate = ? WHERE id = ?", (kd, id))
                    
                elif oc == "loss":
                    wl2[1] += score
                    
                    if wl2[1] <= 0:
                        wl2[1] = 0
                    
                    kd = wl2[0] / (wl2[0] + wl2[1])
                    
                    await db.execute("UPDATE score SET loss = ? WHERE id = ?", (wl2[1], id))
                    await db.execute("UPDATE score SET kd_rate = ? WHERE id = ?", (kd, id))

                await db.commit()
                await db.close()
                return True
            except Exception as e:
                print(e)
                
                try:
                    await db.close()
                except:
                    pass
                
                return False
        else:
            return False
        
    async def get_inventory(self, id: int):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        inv = None
        
        try:
            inv = await db.execute("SELECT inventory FROM items WHERE id = ?", (id, ))
            inv = await inv.fetchall()
            
            await db.close()
            return inv[0][0].split(",")
        except Exception as e:
            print(e)
                
            try:
                await db.close()
            except:
                pass
            
    async def edit_inventory(self, id: int, item: str, act: Literal["add", "remove"]):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        inv = await self.get_inventory(id)
        invstr = ""
        
        if act in ["add", "remove"]:
            try:
                if act == "add":
                    inv.insert(len(inv) - 1, item)
                    
                    for a in inv:
                        if a == "":
                            break
                        else:
                            invstr += f"{a},"
                    
                    await db.execute("UPDATE items SET inventory = ? WHERE id = ?", (invstr, id))
                    
                elif act == "remove":
                    inv.remove(item)
                    
                    for a in inv:
                        if a == "":
                            break
                        else:
                            invstr += f"{a},"
                    
                    await db.execute("UPDATE items SET inventory = ? WHERE id = ?", (invstr, id))

                await db.commit()
                await db.close()
                return True
            except Exception as e:
                print(e)
                
                try:
                    await db.close()
                except:
                    pass
                
                return False
        else:
            return False
    
    async def check_item(self, id: int, item: str):
        inv = await self.get_inventory(id)
        
        if item.isspace() or item == "":
            return False
        else:
            return item in inv
        
    async def get_helditem(self, id: int):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        hitem = ""
        
        try:
            hitem = await db.execute("SELECT held_item FROM items WHERE id = ?", (id, ))
            hitem = await hitem.fetchall()
            await db.close()
            
            return hitem[0][0]
        except Exception as e:
            print(e)
                
            try:
                await db.close()
            except:
                pass
    
    async def edit_helditem(self, id: int, item: str, act: str):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        hitem = await self.get_helditem(id)
        
        if act in ["set", "remove"] or (item.isspace() or item == None):
            try:
                if hitem == item and act == "set":
                    await db.close()
                    return 7
                
                elif act == "set":
                    await db.execute("UPDATE items SET held_item = ? WHERE id = ?", (item, id))
                    await db.commit()
                    
                    await db.close()
                    return 5
                
                elif act == "remove":
                    await db.execute("UPDATE items SET held_item = ? WHERE id = ?", ("None", id))
                    await db.commit()
                    
                    await db.close()
                    return 4
            except Exception as e:
                print(e)
                
                try:
                    await db.close()
                except:
                    pass
                
                return -1
        else:
            return -1
    
    async def get_all_scores(self):
        db = await aiosqlite.connect(self.dir + f"{self.dbname}.db")
        scores = []
        
        try:
            cur = await db.execute("SELECT * FROM score ORDER BY kd_rate")
            for row in await cur.fetchall():
                scores.append(row)
            
            await db.close()
            return scores
        except Exception as e:
            print(e)
            
            try:
                await db.close()
            except:
                pass
            
    async def check_enough_money(self, id: int, amount: int, dest: Literal["wallet", "bank"]):
        if dest in ["wallet", "bank"]:
            monies = self.get_money(id, dest)
            return (monies - amount) >= 0
        else:
            return False