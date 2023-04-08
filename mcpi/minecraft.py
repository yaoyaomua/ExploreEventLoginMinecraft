import os
import math

from .connection import Connection
from .vec3 import Vec3
from .event import BlockEvent, ChatEvent, ProjectileEvent
from .util import flatten

from mcpi.minecraftstuff import Vec3, MinecraftDrawing,MinecraftTurtle
""" Minecraft PI low level api v0.1_1

    Note: many methods have the parameter *arg. This solution makes it
    simple to allow different types, and variable number of arguments.
    The actual magic is a mix of flatten_parameters() and __iter__. Example:
    A Cube class could implement __iter__ to work in Minecraft.setBlocks(c, id).

    (Because of this, it's possible to "erase" arguments. CmdPlayer removes
     entityId, by injecting [] that flattens to nothing)

    @author: Aron Nieminen, Mojang AB"""

""" Updated to include functionality provided by RaspberryJuice:
- getBlocks()
- getDirection()
- getPitch()
- getRotation()
- getPlayerEntityId()
- pollChatPosts()
- setSign()
- spawnEntity()"""

def intFloor(*args):
    return [int(math.floor(x)) for x in flatten(args)]

class CmdPositioner:
    """Methods for setting and getting positions"""
    def __init__(self, connection, packagePrefix):
        self.conn = connection
        self.pkg = packagePrefix

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getPos", id)
        return Vec3(*list(map(float, s.split(","))))

    def setPos(self, id, *args):
        """Set entity position (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setPos", id, args)

    def getTilePos(self, id):
        """Get entity tile position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getTile", id)
        return Vec3(*list(map(int, s.split(","))))

    def setTilePos(self, id, *args):
        """Set entity tile position (entityId:int) => Vec3"""
        self.conn.send(self.pkg + b".setTile", id, intFloor(*args))

    def setDirection(self, id, *args):
        """Set entity direction (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setDirection", id, args)

    def getDirection(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getDirection", id)
        return Vec3(*map(float, s.split(",")))

    def setRotation(self, id, yaw):
        """Set entity rotation (entityId:int, yaw)"""
        self.conn.send(self.pkg + b".setRotation", id, yaw)

    def getRotation(self, id):
        """get entity rotation (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getRotation", id))

    def setPitch(self, id, pitch):
        """Set entity pitch (entityId:int, pitch)"""
        self.conn.send(self.pkg + b".setPitch", id, pitch)

    def getPitch(self, id):
        """get entity pitch (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getPitch", id))

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        self.conn.send(self.pkg + b".setting", setting, 1 if bool(status) else 0)

class CmdEntity(CmdPositioner):
    """Methods for entities"""
    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"entity")
    
    def getName(self, id):
        """Get the list name of the player with entity id => [name:str]
        
        Also can be used to find name of entity if entity is not a player."""
        return self.conn.sendReceive(b"entity.getName", id)

    def remove(self, id):
        self.conn.send(b"entity.remove", id)


class Entity:
    def __init__(self, conn, entity_uuid, typeName):
        self.p = CmdPositioner(conn, b"entity")
        self.id = entity_uuid
        self.type = typeName
    def getPos(self):
        return self.p.getPos(self.id)
    def setPos(self, *args):
        return self.p.setPos(self.id, args)
    def getTilePos(self):
        return self.p.getTilePos(self.id)
    def setTilePos(self, *args):
        return self.p.setTilePos(self.id, args)
    def setDirection(self, *args):
        return self.p.setDirection(self.id, args)
    def getDirection(self):
        return self.p.getDirection(self.id)
    def setRotation(self, yaw):
        return self.p.setRotation(self.id, yaw)
    def getRotation(self):
        return self.p.getRotation(self.id)
    def setPitch(self, pitch):
        return self.p.setPitch(self.id, pitch)
    def getPitch(self):
        return self.p.getPitch(self.id)
    def remove(self):
        self.p.conn.send(b"entity.remove", self.id)


class CmdPlayer(CmdPositioner):
    """Methods for the host (Raspberry Pi) player"""
    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"player")
        self.conn = connection

    def getPos(self):
        return CmdPositioner.getPos(self, [])
    def setPos(self, *args):
        return CmdPositioner.setPos(self, [], args)
    def getTilePos(self):
        return CmdPositioner.getTilePos(self, [])
    def setTilePos(self, *args):
        return CmdPositioner.setTilePos(self, [], args)
    def setDirection(self, *args):
        return CmdPositioner.setDirection(self, [], args)
    def getDirection(self):
        return CmdPositioner.getDirection(self, [])
    def setRotation(self, yaw):
        return CmdPositioner.setRotation(self, [], yaw)
    def getRotation(self):
        return CmdPositioner.getRotation(self, [])
    def setPitch(self, pitch):
        return CmdPositioner.setPitch(self, [], pitch)
    def getPitch(self):
        return CmdPositioner.getPitch(self, [])

class CmdCamera:
    def __init__(self, connection):
        self.conn = connection

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        self.conn.send(b"camera.mode.setNormal", args)

    def setFixed(self):
        """Set camera mode to fixed view"""
        self.conn.send(b"camera.mode.setFixed")

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        self.conn.send(b"camera.mode.setFollow", args)

    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        self.conn.send(b"camera.setPos", args)


class CmdEvents:
    """Events"""
    def __init__(self, connection):
        self.conn = connection

    def clearAll(self):
        """Clear all old events"""
        self.conn.send(b"events.clear")

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.block.hits")
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*e.split(",")) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"events.chat.posts")
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]

    def pollProjectileHits(self):
        """Only triggered by projectiles => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.projectile.hits")
        events = [e for e in s.split("|") if e]
        return [ProjectileEvent.Hit(*e.split(",")) for e in events]


class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi."""
    def __init__(self, connection):
        self.conn = connection

        self.camera = CmdCamera(connection)
        self.entity = CmdEntity(connection)
        self.player = CmdPlayer(connection)
        self.events = CmdEvents(connection)
    def isHit(self,player_name,  targetX, targetY, targetZ):
        """
        Check if the player hit the target block

        :param string player_name: player's name
        :param int targetX: The x coordinate
        :param int targetY: The y coordinate
        :param int targetZ: The z coordinate
        :return: True for hit, None for nothing happened
        """
        player_id = self.getPlayerEntityId(player_name)
        # player_id = self.getPlayerId(player_name)

        events = self.events.pollBlockHits()
        for e in events:
            pos = e.pos
            if pos.x == targetX and pos.y == targetY and pos.z == targetZ and e.entityId == player_id:
                return True

    def hitEvents(self):
        """
        Only triggered by sword

        :return: [BlockEvent]

        example:

        [BlockEvent(BlockEvent.HIT, -4, -1, -10, 1, 640522), BlockEvent(BlockEvent.HIT, 10116, -1, 9559, 1, 640452)]

        player(640522) hit the block(-4, -1, -10) on the up face, player(640452) hit the block(10116, -1, 9559) on the up face

        block faces(up n s w e bottom : 1 2 3 4 5 6)
        """
        blockHits = self.events.pollBlockHits()
        return blockHits

    def getHitEvent(self):
        """
        Get the hitEvent

        :return: int

        example:

        (640452, Vec3(10115,-1,9557), 1)

        hitPlayerID(640452); hitPosition(x, y, z); hitFace：up n s w e bottom : 1 2 3 4 5 6

        x, y, z = mymc.getPlayerPosition(player_name)
        print(x, y, z)
        while True:
            event = mymc.getHitEvent()
            print(event)
            time.sleep(1)
        """
        events = self.events.pollBlockHits()
        for e in events:
            if e == None:
                print('df')
            else:
                # pos = e.pos
                # face = e.face
                # playerID = e.entityId
                # e = (playerID, pos, face)
                return e.face

    def drawPicture(self,x,y,z,s,blocks, facing="S", vertical=False):
        s = s.strip("\n ").split("\n")
        li = s[1:]
        h = int(s[0])
        length = len(li)
        facing = facing.upper()
        if vertical:
            if facing == "S":
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x + j, y + length - i, z - k, blocks.get(li[i][j], "Air"))
            elif facing == "N":
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x - j, y + length - i, z + k, blocks.get(li[i][j], "Air"))
            elif facing == "W":
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x + k, y + length - i, z + j, blocks.get(li[i][j], "Air"))
            else:
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x - k, y + length - i, z - j, blocks.get(li[i][j], "Air"))



        else:
            if facing == "S":
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x + j, y + k, z + i, blocks.get(li[i][j], "Air"))
            elif facing == "N":
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x - j, y + k, z - i, blocks.get(li[i][j], "Air"))
            elif facing == "E":
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x + i, y + k, z - j, blocks.get(li[i][j], "Air"))
            else:
                for k in range(h):
                    for i in range(length):
                        for j in range(len(li[i])):
                            self.setBlock(x - i, y + k, z + j, blocks.get(li[i][j], "Air"))

    def getPlayerPosition(self,player_name):

        player_id = self.getPlayerEntityId(player_name)
        player_pos = self.entity.getTilePos(player_id)
        return player_pos
    def setPlayerPosition(self, player_name, posx, posy, posz):
        """
        Set player position
        :param string player_name: player's name
        :param int posx: The x coordinate
        :param int posy: The y coordinate
        :param int posz: The z coordinate
        """
        player_id = self.getPlayerEntityId(player_name)
        self.entity.setPos(player_id, posx, posy, posz)

    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        return self.conn.sendReceive(b"world.getBlock", intFloor(args))

    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block"""
        return self.conn.sendReceive(b"world.getBlockWithData", intFloor(args)).split(",")

    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        # s = self.conn.sendReceive(b"world.getBlocks", intFloor(args))
        s = self.conn.sendReceive(b"world.getBlocks", *args)
        return s.split(",")

    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        self.conn.send(b"world.setBlock", *args)

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        self.conn.send(b"world.setBlocks", *args)

    def setSign(self, *args):
        """Set a sign (x,y,z,id,data,[line1,line2,line3,line4])

        Wall signs (id=68) require data for facing direction 2=north, 3=south, 4=west, 5=east
        Standing signs (id=63) require data for facing rotation (0-15) 0=south, 4=west, 8=north, 12=east
        @author: Tim Cummings https://www.triptera.com.au/wordpress/"""
        lines = []
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        print(flatargs)
        for flatarg in flatargs[5:]:
            lines.append(flatarg.replace(",", ";").replace(")", "]").replace("(", "["))
        self.conn.send(b"world.setSign", intFloor(flatargs[0:5]) + lines)

    def spawnEntity(self, *args):
        """Spawn entity (x,y,z,id,[data])"""
        return Entity(self.conn, self.conn.sendReceive(b"world.spawnEntity", *args), args[3])

    def spawnParticle(self, *args):
        """Spawn entity (x,y,z,id,[data])"""
        return self.conn.send(b"world.spawnParticle", *args)

    def getNearbyEntities(self, *args):
        """get nearby entities (x,y,z)"""
        entities = []
        # if len(entities)==0:
        #     return entities

        for i in self.conn.sendReceive(b"world.getNearbyEntities", *args).split(","):
            if not i:
                return entities
            name, eid = i.split(":")
            entities.append(Entity(self.conn, eid, name))
        return entities

    def removeEntity(self, *args):
        """Spawn entity (x,y,z,id,[data])"""
        return self.conn.sendReceive(b"world.removeEntity", *args)

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        return int(self.conn.sendReceive(b"world.getHeight", intFloor(args)))

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        ids = self.conn.sendReceive(b"world.getPlayerIds")
        return ids.split("|")

    def getPlayerEntityId(self, name):
        """Get the entity id of the named player => [id:int]"""
        return self.conn.sendReceive(b"world.getPlayerId", name)

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.conn.send(b"world.checkpoint.save")

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint"""
        self.conn.send(b"world.checkpoint.restore")

    def postToChat(self, msg):
        """Post a message to the game chat"""
        self.conn.send(b"chat.post", msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        self.conn.send(b"world.setting", setting, 1 if bool(status) else 0)

    def setPlayer(self, name):
        return self.conn.sendReceive(b"setPlayer", name)

    @staticmethod
    def create(address="localhost", port=4711, debug=False):
        if "JRP_API_HOST" in os.environ:
            address = os.environ["JRP_API_HOST"]
        if "JRP_API_PORT" in os.environ:
            try:
                port = int(os.environ["JRP_API_PORT"])
            except ValueError:
                pass
        return Minecraft(Connection(address, port, debug))


def mcpy(func):
    # these will be created as global variable in module, so not good idea
    # func.__globals__['mc'] = Minecraft.create()
    # func.__globals__['pos'] = func.__globals__['mc'].player.getTilePos()
    # func.__globals__['direction'] = func.__globals__['mc'].player.getDirection()
    func.__doc__ = ("_mcpy :" + func.__doc__) if func.__doc__ else "_mcpy "
    return func
mc = Minecraft.create()

mcDrawing = MinecraftDrawing(mc)


