from flask import Flask, request, jsonify, render_template, redirect
import random
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import DateTime, func
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)
app.debug = True

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:riKras-budqyt-vetva4@34.41.151.108/connections-human:us-central1:connections-gcloud'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#our db
class Profile(db.Model):
    name = db.Column(db.String(25), unique=False, nullable=1)
    score = db.Column(db.Integer, unique=False, nullable=1)
    gamenum = db.Column(db.Integer, nullable=1)
    catnum = db.Column(db.Integer, nullable=1)
    #num = db.Column(db.Integer, unique=False, nullable=1, primary_key=True)
    num = db.Column(DateTime(timezone=True), default=func.now(),primary_key=True)
    result = db.Column(db.String(250), unique=False, nullable=1)
    
    def __repr__(self):
        return f"Name: {self.name}, Game Score: {self.score}, Categories Correct: {self.catnum}, Time: {self.num}, Game Number: {self.gamenum}"
    
profs = []
count = 0
sample = []
x = []
index = 0

lst = [['GRANDE', ' MARS', ' STYLES', ' SWIFT', ' CHANNEL', ' MEANS', ' MEDIUM', ' VEHICLE', ' OUTSIDE', ' REMOTE', ' SLIM', ' SMALL', ' LARGE', ' LEGEND', ' PROOF', ' ROOM'], ['HALL', ' LIBRARY', ' LOUNGE', ' STUDY', ' ASSOCIATE', ' FELLOW', ' PARTNER', ' PEER', ' BUNNY', ' EGG', ' JELLY BEAN', ' PEEP', ' ANIMAL', ' BIRTHMARK', ' SPY', ' UNIT'], ['MASS', ' SEA', ' SLEW', ' TON', ' BUCKLE', ' CAVE', ' COLLAPSE', ' GIVE', ' SHOUT', ' SNAP', ' WAVE', ' WHISTLE', ' BUTTON', ' DANCE', ' FLOP', ' LAUGH'], ['AGENT', ' ASSET', ' MOLE', ' SLEEPER', ' FOOT', ' LINE', ' METER', ' VERSE', ' COUCH', ' IMPLY', ' INTIMATE', ' SUGGEST', ' KELVIN', ' OKAY', ' POTASSIUM', ' THOUSAND'], ['BREAD', ' BUTTER', ' GARLIC', ' PARSLEY', ' BET', ' GAMBLE', ' RISK', ' STAKE', ' ADVENTURE', ' FANTASY', ' FRONTIER', ' TOMORROW', ' BASEBALL', ' CRICKET', ' FRUIT', ' VAMPIRE'], ['HOP', ' JUMP', ' LEAP', ' SPRING', ' CHEST', ' COFFER', ' SAFE', ' VAULT', ' AGE', ' DAY', ' ERA', ' TIME', ' DRIB', ' FLOW', ' REED', ' TANG'], ['AMERICAN', ' BLUE', ' JACK', ' SWISS', ' HAMMER', ' HURDLE', ' JAVELIN', ' POLE', ' CUBAN', ' KITTEN', ' STILETTO', ' WEDGE', ' DATE', ' DUTCH', ' JEOPARDY', ' SPACE'], ['HEADBAND', ' MULLET', ' NEON', ' SPANDEX', ' PIKE', ' SPLIT', ' STRADDLE', ' TUCK', ' ANIMAL', ' GOLDFISH', ' OYSTER', ' RITZ', ' CORPORATE', ' ROPE', ' SALMON', ' WORD'], ['BITTER', ' SALTY', ' SOUR', ' SWEET', ' BRAVE', ' CONFRONT', ' FACE', ' MEET', ' KIND', ' SORT', ' TYPE', ' VARIETY', ' EXPRESSION', ' MANNER', ' ROMANTIC', ' SURREAL'], ['LUMBER', ' PLOD', ' STOMP', ' TRUDGE', ' ELASTIC', ' LIMBER', ' PLASTIC', ' SUPPLE', ' FOIL', ' GLOVE', ' JACKET', ' MASK', ' BASSINET', ' CELLOPHANE', ' HARPOON', ' ORGANISM'], ['FACTORY', ' MILL', ' PLANT', ' SHOP', ' WIND', ' WINE', ' WING', ' WINK', ' CORE', ' RIND', ' SEED', ' STEM', ' FEATHER', ' HEAVY', ' LIGHT', ' MIDDLE'], ['CARAVAN', ' FLEET', ' PARADE', ' TRAIN', ' OLIVE', ' FOREST', ' LIME', ' MINT', ' DEMOCRATIC', ' EROTIC', ' NOBLE', ' SAD', ' BOOK', ' CACTUS', ' HEDGEHOG', ' SKELETON'], ['BARK', ' GROWL', ' HOWL', ' WHINE', ' ARM', ' BRANCH', ' CHAPTER', ' WING', ' CRADLE', ' FONT', ' ROOT', ' SOURCE', ' CLUE', ' FROWN', ' MELLOW', ' PREEN'], ['BADGERS', ' BUGS', ' HOUNDS', ' NAGS', ' ANNIE', ' CABARET', ' CATS', ' COMPANY', ' COMPUTER', ' PIANO', ' SUPER', ' TESTS', ' FISH', ' HARD KNOCKS', ' ROCK', ' THOUGHT'], ['BORE', ' DRAG', ' DRIP', ' DUD', ' BRASS', ' RHYTHM', ' STRING', ' WIND', ' BEAD', ' DROP', ' GLOB', ' TEAR', ' BEAT', ' CHARRED', ' LEAK', ' PEE'], ['KINDLING', ' LOG', ' MATCH', ' TINDER', ' BLOW', ' BUMBLE', ' FLUFF', ' SPOIL', ' DRILL', ' GRINDER', ' ROUTER', ' SAW', ' FRAME', ' HANDLE', ' HINGE', ' LOCK'], ['GRAZE', ' NIBBLE', ' PECK', ' SNACK', ' HUNT', ' TRACK', ' TRAIL', ' STALK', ' BEANS', ' PASTA', ' STOCK', ' VEGETABLES', ' BROAD', ' FORE', ' POD', ' TYPE'], ['CURL', ' LOCK', ' RINGLET', ' TRESS', ' COVERAGE', ' EXPOSURE', ' PRESS', ' PUBLICITY', ' DOM', ' ION', ' NESS', ' SHIP', ' FAMILY', ' FLEA', ' FLYING', ' MEDIA'], ['CROC', ' LOAFER', ' MOCCASIN', ' SLIPPER', ' BOA', ' HEADDRESS', ' PILLOW', ' SHUTTLECOCK', ' BASIC', ' JAVA', ' PYTHON', ' RUBY', ' COBRA', ' INSPIRATION', ' LIGHTNING', ' UNION'], ['MONITOR', ' SURVEY', ' TRACK', ' WATCH', ' BEACH', ' DESERT', ' HOURGLASS', ' PLAYGROUND', ' BAKE', ' BROIL', ' LIGHT', ' TIMER', ' BLUR', ' OASIS', ' PULP', ' SUEDE'], ['BRUSH', ' GRAZE', ' KISS', ' SKIM', ' ODD', ' PERFECT', ' PRIME', ' WHOLE', ' OYSTER', ' PLUM', ' SOY', ' XO', ' CLAW', ' FRUIT', ' HUG', ' WITNESS'], ['EGG', ' GOAD', ' SPUR', ' URGE', ' JAWBREAKER', ' MEATBALL', ' MOZZARELLA', ' ORANGE', ' DAIRY', ' FROZEN', ' PRODUCE', ' SNACK', ' BANANAS', ' FIGURE', ' FISH', ' STEADY'], ['DROP', ' ECHO', ' FREEZE', ' LAG', ' MIME', ' PRISONER', ' REFEREE', ' SAILOR', ' GENIE', ' MONKEY', ' PARROT', ' PRINCESS', ' APOLLO', ' CANDLES', ' FANTASTIC', ' SAMURAI'], ['BUZZ', ' DRONE', ' HUM', ' PURR', ' BARGE', ' DORY', ' SCOW', ' SLOOP', ' AMERICA', ' HOOK', ' MORGAN', ' NEMO', ' AUTO', ' BUREAU', ' DEMO', ' PLUTO'], ['CANARY', ' FINK', ' RAT', ' SNITCH', ' JAM', ' PACK', ' SQUEEZE', ' STUFF', ' CAT', ' COW', ' MOUNTAIN', ' TRIANGLE', ' BUTTER', ' DRAGON', ' FIRE', ' HORSE'], ['REWIND', ' SHUFFLE', ' SKIP', ' STOP', ' AIR', ' RUN', ' SCREEN', ' SHOW', ' BATH', ' CARD', ' CURTAIN', ' PICTURE', ' EON', ' ETHER', ' NET', ' TOW'], ['ARROW', ' BOW', ' QUIVER', ' TARGET', ' BRIDGE', ' GIN', ' SPIT', ' WAR', ' BELT', ' CLOCK', ' DECK', ' SLUG', ' ANCHOR', ' DRAGON', ' HEART', ' ROSE'], ['CRAB', ' RAY', ' SPONGE', ' SQUID', ' CIRCLE', ' DIAMOND', ' SQUARE', ' TRIANGLE', ' BOB', ' CROSS', ' HOOK', ' WEAVE', ' FEAST', ' FREE', ' PANTS', ' THAT'], ['BRIGHT', ' FLASHY', ' GARISH', ' LOUD', ' GAS', ' STINKER', ' TOOT', ' WIND', ' DIRTY', ' HONEY', ' PLATINUM', ' STRAWBERRY', ' HUG', ' OF', ' OXYGEN', ' ZERO'], ['BROTHER', ' LORD', ' PLEASE', ' SHEESH', ' BISHOP', ' CARDINAL', ' PASTOR', ' PRIOR', ' HEART', ' MADONNA', ' PRINCE', ' QUEEN', ' DELI', ' NIECE', ' ROAM', ' SOUL'], ['COCOA', ' COFFEE', ' MATE', ' TEA', ' BORING', ' DULL', ' MUNDANE', ' VANILLA', ' ACT', ' BIT', ' ROUTINE', ' SET', ' DIRTY', ' DRY', ' TWIST', ' UP'], ['AGENCY', ' COMPANY', ' ENTERPRISE', ' FIRM', ' COOP', ' PEN', ' STABLE', ' STY', ' FLUFFY', ' REX', ' ROVER', ' SPOT', ' INK', ' LACK', ' OLD', ' RANGE'], ['BREAK', ' HOLIDAY', ' LEAVE', ' RECESS', ' BUCKLE', ' HOLE', ' LOOP', ' STRAP', ' HOLEY', ' HOLI', ' HOLY', ' WHOLLY', ' DOG', ' DRIFT', ' HOLLY', ' SANDAL'], ['CLIP', ' CUT', ' PARE', ' TRIM', ' BUILT', ' JACKED', ' RIPPED', ' SWOLE', ' BUFF', ' FAN', ' LOVER', ' NUT', ' BRAIN', ' PRUNE', ' PUG', ' WALNUT'], ['CHEER', ' GLEE', ' FESTIVITY', ' MIRTH', ' BAND', ' CATERER', ' FLORIST', ' OFFICIANT', ' CHOIR', ' FIRE', ' LIAR', ' FRYER', ' BARBECUE', ' ORCHESTRA', ' SNAKE', ' TAR'], ['BANG', ' HAMMER', ' POUND', ' SLAM', ' CHRONICLE', ' HERALD', ' REGISTER', ' SUN', ' BANANA', ' CROISSANT', ' MOON', ' SICKLE', ' FEATHER', ' FLOWER', ' MUSHROOM', ' STAR'], ['PITCH', ' PLUG', ' PROMOTE', ' PUSH', ' COUPLE', ' ITEM', ' PAIR', ' THING', ' AD', ' ALL', ' DEUCE', ' LOVE', ' BREAD', ' DRAGON', ' JACK', ' PASSION'], ['CREST', ' PEAK', ' SUMMIT', ' VERTEX', ' CELL', ' CONTACT', ' DIGITS', ' NUMBER', ' BABY', ' MINI', ' POCKET', ' TOY', ' BAG', ' BOARD', ' RACKS', ' TILES'], ['ACHE', ' BURN', ' SMART', ' STING', ' GUARD', ' MIND', ' TEND', ' WATCH', ' BRAIN', ' COURAGE', ' HEART', ' HOME', ' ANSWER', ' TWO', ' WRIST', ' WRONG'], ['BALL', ' BASE', ' BAT', ' GLOVE', ' BLOW', ' LICK', ' SOCK', ' STRIKE', ' BOOT', ' IRON', ' THIMBLE', ' TOP HAT', ' BAD', ' BUGS', ' DUST', ' HONEY'], ['BIG', ' HOT', ' IN', ' POPULAR', ' CHARACTER', ' GLYPH', ' ICON', ' SYMBOL', ' ASSESS', ' CHARGE', ' FINE', ' LEVY', ' HANDSOME', ' HIPPO', ' LEGEND', ' LIPID'], ['CALCULATOR', ' CALENDAR', ' CAMERA', ' CLOCK', ' CONE', ' IRIS', ' LENS', ' PUPIL', ' DADA', ' GRAMMY', ' MUM', ' POPPY', ' EXPOSE', ' PATE', ' RESUME', ' ROSE'], ['COIN', ' CREATE', ' DEVISE', ' INVENT', ' FINE', ' PRIME', ' QUALITY', ' STERLING', ' AT', ' DOLLAR', ' PERCENT', ' POUND', ' BAR', ' BUCK', ' TIME', ' TORCH'], ['BATON', ' SCEPTER', ' STAFF', ' WAND', ' CAVITY', ' CROWN', ' FILLING', ' PLAQUE', ' APPROVED', ' PAID', ' URGENT', ' VOID', ' GAP', ' LEAP', ' LIGHT', ' SCHOOL'], ['FLEECE', ' HOSE', ' ROB', ' STIFF', ' CANDLE', ' CRAYON', ' HONEYCOMB', ' SEAL', ' CABIN', ' ENGINE', ' NOSE', ' WING', ' BULB', ' EAR', ' HEAD', ' STALK'], ['DIP', ' DROP', ' FALL', ' SINK', ' BLAZE', ' FLY', ' RACE', ' TEAR', ' MODERN', ' SALSA', ' SWING', ' TAP', ' BOOM', ' CARROT', ' SHOWER', ' TALK'], ['CHERRY', ' FUDGE', ' NUTS', ' SPRINKLES', ' DESERT', ' DITCH', ' MAROON', ' STRAND', ' CURSES', ' DARN', ' RATS', ' SHOOT', ' FUZZY', ' PEPPERS', ' SEASHELLS', ' WOODCHUCK'], ['GRANDSTAND', ' PEACOCK', ' POSTURE', ' STRUT', ' MAIN', ' PARAMOUNT', ' PRIME', ' SUPREME', ' BLUE', ' GREEN', ' WHITE', ' YELLOW', ' CHAIN', ' COVER', ' LOVE', ' SCARLET'], ['MEAN', ' MEDIAN', ' MODE', ' RANGE', ' BASE', ' BOND', ' ELEMENT', ' SOLUTION', ' AWFUL', ' PRETTY', ' RATHER', ' REAL', ' GLASS', ' GROSS', ' KING', ' STERN'], ['CON', ' DUPE', ' FOOL', ' TRICK', ' DOPE', ' SCOOP', ' SKINNY', ' WORD', ' CANT', ' LEAN', ' LIST', ' SLOPE', ' BOOB', ' EGGSHELL', ' GIGGLE', ' HELLO'], ['BALLOT', ' ROSTER', ' SLATE', ' TICKET', ' BUFFER', ' CUSHION', ' PAD', ' SHIELD', ' CAPSULE', ' CREAM', ' SYRUP', ' TABLET', ' COAT', ' GREEN', ' POD', ' SOUP'], ['BILL', ' CHECK', ' INVOICE', ' TAB', ' PINCH', ' ROB', ' STEAL', ' SWIPE', ' BUCK', ' BULL', ' JACK', ' TOM', ' JEAN', ' PANT', ' SHORT', ' TIGHT'], ['BADGE', ' INVITE', ' PASS', ' TICKET', ' CHAIR', ' DIRECT', ' LEAD', ' RUN', ' CENTER', ' END', ' SAFETY', ' TACKLE', ' HOLD', ' PUNT', ' STALL', ' TABLE'], ['ISSUE', ' MATTER', ' POINT', ' SUBJECT', ' CHAPTER', ' PERIOD', ' PHASE', ' STAGE', ' DASH', ' SHOCK', ' TANK', ' WHEEL', ' BLEW', ' CHORAL', ' READ', ' ROWS'], ['GAS', ' LIQUID', ' PLASMA', ' SOLID', ' GREAT', ' HERO', ' ICON', ' LEGEND', ' PHAT', ' PHEW', ' PHILLY', ' PHISH', ' ELEVATOR', ' FEVER', ' PERFECT', ' SALES'], ['CHARM', ' CURSE', ' HEX', ' SPELL', ' FLUE', ' GRATE', ' LOG', ' POKER', ' CARDS', ' CHIPS', ' DICE', ' SLOTS', ' CRUMBLE', ' MELT', ' SHRED', ' SLICE'], ['BROOM', ' MOP', ' RAG', ' SPONGE', ' SALT', ' FAT', ' ACID', ' HEAT', ' DUST', ' PEPPER', ' POLLEN', ' SMOKE', ' MAGNUM', ' MONK', ' SHAFT', ' TRACY'], ['BASKETBALL', ' CARROT', ' GOLDFISH', ' PUMPKIN', ' POLE', ' ROD', ' STAFF', ' STICK', ' CART', ' CLUB', ' HOLE', ' TEE', ' CIRCLE', ' HORSESHOE', ' PITCHFORK', ' TRIANGLE'], ['ALPHABET', ' AMAZON', ' APPLE', ' META', ' BAR', ' FINAL', ' ORAL', ' PHYSICAL', ' BEAUTY', ' GEM', ' MARVEL', ' PEACH', ' BABY', ' EYE', ' SWEET', ' WISDOM'], ['FUNK', ' MUSK', ' ODOR', ' TANG', ' ROCK', ' SWAY', ' SWING', ' WAVE', ' AFRO', ' BONE', ' FIGHT', ' LOCK', ' CRYSTAL', ' DISCO', ' FOUL', ' GUTTER'], ['JOSH', ' KID', ' RIB', ' TEASE', ' HEIGHT', ' MAX', ' PEAK', ' TOP', ' DOZEN', ' GROSS', ' PAIR', ' SCORE', ' ADULT', ' KISS', ' TEN', ' TIMES'], ['BOW', ' BOX', ' CARD', ' WRAPPING', ' BLOCK', ' MATCH', ' MESSAGE', ' SWIPE', ' FIRE', ' LIT', ' SICK', ' TIGHT', ' BREAK', ' CHARM', ' DUCK', ' STRIKE'], ['FLOAT', ' FLY', ' GLIDE', ' SOAR', ' BUG', ' MIKE', ' TAP', ' WIRE', ' CHECK', ' MARK', ' TICK', ' X', ' 40', ' COLE', ' PAIN', ' TIP'], ['BREAD', ' BACON', ' LETTUCE', ' TOMATO', ' BLOCK', ' CLOG', ' JAM', ' STOP', ' DOUBLE', ' HIT', ' RUN', ' WALK', ' FRY', ' TALK', ' WONDER', ' WORLD'], ['PLANT', ' SEED', ' WATER', ' WEED', ' CAESAR', ' GREEK', ' GREEN', ' WEDGE', ' FEUD', ' MILLIONAIRE', ' PYRAMID', ' WHEEL', ' WAY', ' WEE', ' WHY', ' WHOA'], ['CLUB', ' GROUP', ' PARTY', ' TEAM', ' CLARITY', ' DEFINITION', ' DETAIL', ' RESOLUTION', ' CHAMPAGNE', ' DIJON', ' NICE', ' TOURS', ' BALL', ' COUNTDOWN', ' FIREWORKS', ' KISS'], ['ORCA', ' PANDA', ' SKUNK', ' ZEBRA', ' CHAIN', ' SERIES', ' STRING', ' TRAIN', ' BASS', ' DOVE', ' DESERT', ' WIND', ' BEAR', ' SAND', ' SPEED', ' TOURIST'], ['CROP', ' POLO', ' TANK', ' TEE', ' BAD', ' FLY', ' FRESH', ' RAD', ' BEE', ' EX', ' GEE', ' JAY', ' BOY', ' BY', ' CURIOUS', ' SAINT'], ['BUMPER', ' HOOD', ' TIRE', ' TRUNK', ' BOLT', ' DART', ' DASH', ' ZIP', ' CARDINAL', ' JAY', ' LARK', ' SWIFT', ' HANCOCK', ' HOLIDAY', ' MONK', ' PARKER'], ['MESSAGE', ' OMEN', ' SIGN', ' WARNING', ' GEN', ' MS', ' PROF', ' REV', ' CHARCOAL', ' INK', ' PAINT', ' PASTEL', ' BELL', ' BLACK', ' DR', ' GHOST'], ['ALLEY', ' DRIVE', ' LANE', ' STREET', ' FOLIO', ' LEAF', ' PAGE', ' SHEET', ' CHECK', ' CURB', ' LIMIT', ' STEM', ' BLOW', ' HOLD', ' PICK', ' THUMB'], ['BABY', ' BOO', ' DEAR', ' LOVE', ' LINE', ' POINT', ' RAY', ' SEGMENT', ' ENERGY', ' FIRE', ' JUICE', ' ZIP', ' AGENT', ' CODE', ' SANTA', ' SAUCE'], ['LIGHT', ' MELLOW', ' MILD', ' SOFT', ' BELLY', ' CHOP', ' HOCK', ' SHOULDER', ' CROWN', ' ROBE', ' TABLET', ' TORCH', ' CANDLE', ' DANDELION', ' DICE', ' EYELASH'], ['BOAT', ' CAR', ' PLANE', ' TRAIN', ' DOWN', ' GAME', ' IN', ' ON BOARD', ' DASH', ' DROP', ' PINCH', ' SPLASH', ' BLUE', ' GOOSE', ' RASP', ' STRAW'], ['ANGEL', ' CLOWN', ' PIRATE', ' WITCH', ' COMB', ' HIVE', ' HONEY', ' WAX', ' PERIOD', ' SPELL', ' STRETCH', ' WHILE', ' DEAR', ' HAIR', ' HOARSE', ' WAIL'], ['DRYER', ' HAMPER', ' IRON', ' WASHER', ' DIRECT', ' GUIDE', ' LEAD', ' STEER', ' IODINE', ' IOTA', ' MYSELF', ' ONE', ' DEATH', ' HIDDEN', ' SILICON', ' UNCANNY'], ['BUZZ', ' CALL', ' DIAL', ' RING', ' APPENDIX', ' CHAPTER', ' INDEX', ' PREFACE', ' DINKY', ' LITTLE', ' MINUTE', ' SLIGHT', ' ITCHY', ' JERRY', ' PINKY', ' SPEEDY'], ['BELT', ' BRACELET', ' TIE', ' WATCH', ' BIT', ' JOKE', ' ROUTINE', ' SKETCH', ' APPEAL', ' CHARM', ' DRAW', ' PULL', ' CANINE', ' FREIGHT', ' OFTEN', ' STONE'], ['FLASH', ' JIFFY', ' SECOND', ' WINK', ' CHIEF', ' FIRST', ' MAIN', ' PRINCIPAL', ' BROADWAY', ' FIFTH', ' MADISON', ' PARK', ' AMATEUR', ' ELEVENTH', ' HAPPY', ' RUSH'], ['BANK', ' SAVE', ' STASH', ' STORE', ' GALL', ' GUTS', ' NERVE', ' STONES', ' CARROT', ' COAL', ' SNOW', ' STICKS', ' BONE', ' BUSINESS', ' GIRL', ' PAGES'], ['HOE', ' PLOW', ' RAKE', ' SICKLE', ' PLOT', ' PLOY', ' RUSE', ' TRICK', ' AMUSE', ' DELIGHT', ' PLEASE', ' TICKLE', ' BANG', ' PLOP', ' SPLASH', ' THUD'], ['CRAB', ' CRANK', ' GROUCH', ' GRUMP', ' CROUCH', ' DUCK', ' SQUAT', ' STOOP', ' ANTHEM', ' FLAG', ' MOTTO', ' SEAL', ' CHEAT', ' CROOK', ' QUACK', ' SHARK'], ['BADGER', ' BUG', ' HOUND', ' NAG', ' ARENA', ' BOWL', ' DOME', ' FIELD', ' DIVIDE', ' FORK', ' PART', ' SPLIT', ' FOX', ' LINING', ' SCREEN', ' SPOON'], ['BUNKER', ' FAIRWAY', ' GREEN', ' ROUGH', ' ENOUGH', ' MERCY', ' STOP', ' UNCLE', ' BAWDY', ' BLUE', ' COARSE', ' RISQUE', ' BOUGH', ' COUGH', ' DOUGH', ' TOUGH'], ['CLOUD', ' FOG', ' HAZE', ' MIST', ' SHADOW', ' TAIL', ' TRACK', ' TRAIL', ' BALL', ' BUMPER', ' FLIPPER', ' PLUNGER', ' ICE', ' IRE', ' FIN', ' NETHER'], ['CHIFFON', ' SATIN', ' SILK', ' VELVET', ' PERCH', ' ROOST', ' SETTLE', ' LAND', ' EYELET', ' LACE', ' SOLE', ' TONGUE', ' BABY', ' BLOW', ' PACKAGE', ' SPEECH'], ['BANK', ' BED', ' DELTA', ' MOUTH', ' BREEZE', ' CINCH', ' PICNIC', ' SNAP', ' COIL', ' SPIRAL', ' TWIST', ' WIND', ' BOUND', ' LEAP', ' SPRING', ' VAULT'], ['FLOAT', ' SHAKE', ' SPLIT', ' SUNDAE', ' BOLT', ' NAIL', ' RIVET', ' SCREW', ' CORN', ' OLIVE', ' PALM', ' PEANUT', ' FINGERS', ' NOTE', ' RICE', ' WICKET'], ['EBB', ' FADE', ' FLAG', ' WANE', ' PURE', ' SHEER', ' TOTAL', ' UTTER', ' AIR', ' SPEAK', ' STATE', ' VOICE', ' BANNER', ' PRINCE', ' STARK', ' WAYNE'], ['HI', ' LA', ' MA', ' OK', ' BET', ' E', ' HALLMARK', ' USA', ' ALFA', ' BRAVO', ' ROMEO', ' TANGO', ' BOO', ' POM', ' TOM', ' YO'], ['CLEF', ' NOTE', ' REST', ' STAFF', ' BULL', ' CRAB', ' SCALES', ' TWINS', ' CAPITOL', ' COLUMBIA', ' VIRGIN', ' ISLAND', ' CAN', ' GEM', ' LIB', ' TAU'], ['BIG', ' GIANT', ' GREAT', ' HUGE', ' FICTION', ' HUMOR', ' POETRY', ' TRAVEL', ' CHEERS', ' EUPHORIA', ' FELICITY', ' GLEE', ' CONSTRUCTION', ' FRASIER', ' PAPER', ' WHOOPING'], ['BAGUETTE', ' BUN', ' LOAF', ' ROLL', ' CLINCH', ' GUARANTEE', ' LOCK', ' SECURE', ' CHIP', ' MARK', ' NICK', ' SCRATCH', ' HAIR', ' LETTUCE', ' STATE', ' STEAM'], ['CABLE', ' ELECTRIC', ' GAS', ' WATER', ' ACOUSTIC', ' AUDITORY', ' HEARD', ' SONIC', ' COUPLE', ' HITCH', ' LINK', ' TIE', ' AMP', ' FIRE', ' HYPE', ' PUMP'], ['BASKET', ' BIN', ' CHEST', ' HAMPER', ' BAND', ' CIRCLE', ' HOOP', ' RING', ' CAP', ' CHECK', ' CURB', ' LIMIT', ' NBA', ' PAPER', ' PEARL', ' TRAFFIC'], ['MALL', ' MARKET', ' OUTLET', ' STORE', ' SHAVE', ' THREAD', ' TWEEZE', ' WAX', ' CUT', ' PIECE', ' SHARE', ' TAKE', ' ALLEN', ' CRESCENT', ' MONKEY', ' SOCKET'], ['DODGE', ' DUCK', ' ESCAPE', ' SKIRT', ' BIRDS', ' NOTORIOUS', ' REBECCA', ' ROPE', ' GOOSE', ' HOBBES', ' ROBIN', ' WATSON', ' COTTAGE', ' CREAM', ' SAY', ' STRING'], ['ARCH', ' BALL', ' SOLE', ' TOE', ' BASS', ' HARP', ' HORN', ' ORGAN', ' COME', ' DOWN', ' SIT', ' STAY', ' DOG', ' HEEL', ' JERK', ' SNAKE'], ['BEDROOM', ' DEN', ' KITCHEN', ' STUDY', ' ATOLL', ' BAR', ' ISLAND', ' KEY', ' CRAM', ' JAM', ' PACK', ' STUFF', ' BAG', ' COUNTER', ' DIP', ' SPROUT'], ['HUM', ' SING', ' SCAT', ' WHISTLE', ' COUNT', ' GROSS', ' SUM', ' TOTAL', ' LIME', ' MINT', ' RUM', ' SODA', ' GLUE', ' GUM', ' TAPE', ' STICK'], ['CITY', ' COUNTY', ' TOWN', ' VILLAGE', ' CHOP', ' GRIND', ' PULSE', ' PUREE', ' CAPITAL', ' EQUITY', ' INTEREST', ' STOCK', ' IVY', ' JUSTICE', ' LITTLE', ' PREMIER'], ['HIDDEN', ' PRIVATE', ' REMOTE', ' SECRET', ' AMOUNT', ' NUMBER', ' QUANTITY', ' VOLUME', ' CANAL', ' CHANNEL', ' SOUND', ' STRAIT', ' 96', ' MOW', ' NOON', ' SIS'], ['KNOCK', ' PAN', ' ROAST', ' SLAM', ' ALONE', ' CATFISH', ' CHOPPED', ' SURVIVOR', ' FIAT', ' JAGUAR', ' MINI', ' RAM', ' BACHELOR', ' LILY', ' MAXI', ' MOUSE'], ['PASTY', ' PIE', ' TART', ' TURNOVER', ' BOUQUET', ' PARFAIT', ' RAGOUT', ' RAPPORT', ' JAPAN', ' POLAND', ' TUNISIA', ' TURKEY', ' BIRD', ' CURRY', ' JAMES', ' JORDAN'], ['CANYON', ' GULCH', ' PASS', ' RAVINE', ' GORGE', ' GULP', ' SCARF', ' WOLF', ' APPLE', ' BASHFUL', ' MIRROR', ' QUEEN', ' CHEN', ' CLARK', ' COWL', ' CRAVEN'], ['CANINE', ' FANG', ' MOLAR', ' TUSK', ' CHIC', ' HIP', ' HOT', ' IN', ' FLOSS', ' ROBOT', ' VOGUE', ' WORM', ' LEECH', ' STRAW', ' VACUUM', ' VAMPIRE'], ['CARDINAL', ' LAMA', ' MONK', ' PASTOR', ' BABOON', ' BONOBO', ' GIBBON', ' GORILLA', ' MANGO', ' MINT', ' TAMARIND', ' TOMATO', ' APE', ' MIME', ' MIRROR', ' PARROT'], ['BIRTH', ' CREATION', ' DAWN', ' START', ' AUGUST', ' GRAND', ' NOBLE', ' REGAL', ' MARCH', ' STEP', ' STRIDE', ' TREAD', ' EARTH', ' GROUNDHOG', ' LABOR', ' MAY'], ['GANDER', ' GLANCE', ' GLIMPSE', ' LOOK', ' ACT', ' BLUFF', ' CHARADE', ' FRONT', ' CLIFF', ' CRAG', ' LEDGE', ' RIDGE', ' PEAK', ' PEEK', ' PEKE', ' PIQUE'], ['DIPS', ' LUNGES', ' PLANKS', ' SQUATS', ' BEST', ' CHEERS', ' REGARDS', ' THANKS', ' CARDS', ' JAYS', ' NATS', ' YANKS', ' BANKS', ' MOSS', ' TAYLOR', ' WARREN'], ['BULL', ' HOGWASH', ' NONSENSE', ' ROT', ' DIRECT', ' GUIDE', ' LEAD', ' STEER', ' BUFFALO', ' DEER', ' FISH', ' MOOSE', ' DANE', ' LAKE', ' SEAL', ' WHITE'], ['EW', ' ICK', ' PU', ' UGH', ' O', ' OK', ' US', ' W', ' HAI', ' JA', ' SI', ' DA', ' OUI', ' WE', ' WEE', ' WII'], ['ANGER', ' FEAR', ' HAPPINESS', ' SURPRISE', ' BEHOLD', ' PRESTO', ' TADA', ' VOILA', ' GET', ' LAND', ' SECURE', ' WIN', ' ADAM', ' CARPENTER', ' FIRE', ' RED'], ['LETTER', ' PARAGRAPH', ' SENTENCE', ' WORD', ' FEATURE', ' HALLMARK', ' STAMP', ' TRAIT', ' CARD', ' CLOWN', ' CUTUP', ' JOKER', ' BOOK', ' TABLE', ' TEA', ' TREE'], ['FORD', ' GRANT', ' LINCOLN', ' WILSON', ' COACH', ' GM', ' PLAYER', ' SCOUT', ' BMW', ' HONDA', ' JAGUAR', ' SUBARU', ' AUTO', ' POST', ' SEMI', ' SUB'], ['LIGHT', ' SHORT', ' SPARE', ' THIN', ' BALL', ' BLAST', ' KICK', ' RIOT', ' BOOM', ' DOLLY', ' LENS', ' TRIPOD', ' CLUE', ' GRIP', ' LIFE', ' ROOM'], ['ANISE', ' DILL', ' NUTMEG', ' SAGE', ' BRIGHT', ' QUICK', ' SHARP', ' SMART', ' AXE', ' DEGREE', ' OLD SPICE', ' SECRET', ' CLUB', ' MACE', ' SPEAR', ' SWORD'], ['DIET', ' EXERCISE', ' FRESH AIR', ' SLEEP', ' COMPOSE', ' FORWARD', ' REPLY ALL', ' SEND', ' RADIOLAB', ' SERIAL', ' UP FIRST', ' WTF', ' BLACK', ' DIVINE', ' PROP', ' SKETCH'], ['FLIP-FLOP', ' SUNSCREEN', ' TOWEL', ' UMBRELLA', ' CURLY', ' SHOESTRING', ' WAFFLE', ' WEDGE', ' HEDGE', ' SEE-SAW', ' WAVER', ' YO-YO', ' BREEZE', ' MARY', ' MULE', ' RUSSIAN'], ['CHIME', ' DING', ' PING', ' RING', ' RAT', ' SING', ' SNITCH', ' SQUEAL', ' CAMP', ' DIVISION', ' FACTION', ' WING', ' BING', ' EDGE', ' SURFACE', ' WORD'], ['BOND', ' CD', ' OPTION', ' STOCK', ' LP', ' PLATTER', ' VINYL', ' WAX', ' BOUILLON', ' DIE', ' ICE', ' SUGAR', ' FUNNY', ' HERRING', ' SOUP', ' WISH'], ['EVEN', ' LEVEL', ' STABLE', ' STEADY', ' LANCE', ' PIN', ' SKEWER', ' SPIT', ' BILLBOARD', ' PITCHFORK', ' ROLLING STONE', ' SPIN', ' UNIFORM', ' BICYCLE', ' TRILOGY', ' QUADRANT'], ['DRILL', ' PRACTICE', ' STUDY', ' TRAIN', ' HOSE', ' PIPE', ' STRAW', ' TUBE', ' CANDLESTICK', ' KNIFE', ' ROPE', ' WRENCH', ' CIGARETTE', ' BIKE', ' TICKET', ' SPORTS'], ['HOWEVER', ' STILL', ' THOUGH', ' YET', ' HEAR', ' KNOCK', ' THERE', ' TUT', ' ARE', ' SEE', ' WHY', ' YOU', ' FAMILY', ' FLUSH', ' JELLY', ' WE'], ['BURN', ' KINDLE', ' LIGHT', ' TORCH', ' DATA', ' INFO', ' INTEL', ' NEWS', ' DELL', ' GLEN', ' HOLLOW', ' VALLEY', ' APPLE', ' COMPUTER', ' PLANET', ' REACTOR'], ['FOLLOW', ' LIKE', ' SHARE', ' SUBSCRIBE', ' DARN', ' HEM', ' SEAM', ' SEW', ' ER', ' HOUSE', ' RATCHED', ' SCRUBS', ' ERM', ' UH', ' UM', ' WELL'], ['DAISY', ' ROSE', ' TULIP', ' VIOLET', ' BARN', ' CHICKEN', ' FARMER', ' TRACTOR', ' ASTER', ' CARPENTER', ' CRAVEN', ' WAN', ' DUST', ' LIFE', ' SPORTS', ' YELLOW'], ['BEAK', ' FEATHER', ' TALON', ' WING', ' FLASH', ' HEARTBEAT', ' SECOND', ' WINK', ' BAMBOO', ' DRAGON', ' SEASON', ' WIND', ' BELLY', ' HOT', ' PANIC', ' SNOOZE'], ['HASH', ' JUMBLE', ' MEDLEY', ' STEW', ' CHALLENGE', ' CONFRONT', ' FACE', ' OPPOSE', ' BROOD', ' CLUTCH', ' HATCH', ' LITTER', ' BODY', ' BRIDGE', ' FRET', ' NECK'], ['SIGHT', ' SMELL', ' TASTE', ' TOUCH', ' DRESS', ' LOOK', ' MANNER', ' STYLE', ' DITTO', ' LIKEWISE', ' SAME', ' SECOND', ' BLUE', ' HARVEST', ' NEW', ' SAILOR'], ['BRASS', ' CHEEK', ' GALL', ' NERVE', ' COPPER', ' GOLD', ' NICKEL', ' SILVER', ' MERCURY', ' SKY', ' SPARKS', ' LIBERTY', ' CARS', ' ELEPHANTS', ' SWIMMERS', ' TREES'], ['BUILD', ' GROW', ' SWELL', ' MOUNT', ' ACES', ' KEEN', ' NEATO', ' NIFTY', ' FOAM', ' FROTH', ' HEAD', ' LATHER', ' BUBBLE', ' GLOBE', ' MARBLE', ' PEARL'], ['FUTURE', ' PAST', ' PERFECT', ' PRESENT', ' GOODNESS', ' HEAVENS', ' LORD', ' MERCY', ' DRUMMER', ' LADY', ' RING', ' SWAN', ' CORN', ' COUGH', ' MAPLE', ' SIMPLE'], ['COLONY', ' HERD', ' PRIDE', ' SCHOOL', ' CRANNY', ' NICHE', ' NOOK', ' RECESS', ' CLASSIC', ' DEFINITIVE', ' MODEL', ' TEXTBOOK', ' BACKPACK', ' BIGWIG', ' DOWNTOWN', ' RAGTAG'], ['FOCUS', ' RING', ' SILENT', ' VIBRATE', ' DRIVE', ' INSPIRE', ' MOTIVATE', ' SPUR', ' CONNECTION', ' FEELINGS', ' SPARK', ' VIBE', ' CANDY', ' COPY', ' KNOCKS', ' SELTZER'], ['CHILL', ' HANG', ' LOAF', ' LOUNGE', ' BANGER', ' BOP', ' GROOVE', ' JAM', ' MASH', ' ROAST', ' SCONE', ' TRIFLE', ' BIND', ' PICKLE', ' SCRAPE', ' SPOT'], ['BOWL', ' DISH', ' PLATE', ' SAUCER', ' BALONEY', ' BUNK', ' CROCK', ' TRIPE', ' CUP', ' HOOK', ' STRAP', ' WIRE', ' LASER', ' RADAR', ' SCUBA', ' SPAM'], ['DEN', ' HIVE', ' LAIR', ' NEST', ' CLOUD', ' METAVERSE', ' NET', ' WEB', ' EQUAL', ' EVEN', ' FAIR', ' JUST', ' GOOD', ' IMPOSSIBLE', ' NOTHING', ' WARREN'], ['FABRICATE', ' FAKE', ' FIX', ' FORGE', ' FIDDLESTICKS', ' FIE', ' FRICK', ' FUDGE', ' FARGO', ' FIREFLY', ' FLEABAG', ' FLIPPER', ' FASHION', ' FOOD', ' FORWARD', ' FRIENDS'], ['BORE', ' DRAG', ' SNOOZE', ' YAWN', ' BREEZE', ' DRAFT', ' GUST', ' PUFF', ' BITE', ' KICK', ' TANG', ' ZIP', ' BOXER', ' GOGGLE', ' PANT', ' TONG'], ['BOO', ' HISS', ' JEER', ' RASPBERRY', ' BOMB', ' DUD', ' FLOP', ' LEMON', ' DESERT', ' GHOST', ' IGNORE', ' JILT', ' BOTTOM', ' CANDY', ' GARDEN', ' STAR'], ['FRIDAY', ' SATURDAY', ' SUNDAY', ' THURSDAY', ' ROT', ' SOUR', ' SPOIL', ' TURN', ' FESTER', ' LURCH', ' THING', ' WEDNESDAY', ' CAT', ' CHANCE', ' LIP', ' TUESDAY'], ['FILE', ' HAMMER', ' LEVEL', ' SAW', ' JERK', ' TUG', ' WRENCH', ' YANK', ' COPY', ' FIND', ' PRINT', ' SAVE', ' BABE', ' BEETHOVEN', ' CHARLOTTE', ' WILLY'], ['BOTTOM', ' BUNS', ' SEAT', ' TAIL', ' CORD', ' CRADLE', ' DIAL', ' HANDSET', ' CRIB', ' DIGS', ' JOINT', ' PAD', ' BOOTY', ' LOOT', ' SPOILS', ' SWAG'], ['FAVA', ' KIDNEY', ' LIMA', ' PINTO', ' LAGOS', ' LIMERICK', ' LINCOLN', ' LUXOR', ' LINE', ' METER', ' RHYME', ' VERSE', ' CREATOR', ' DUDE', ' RAPPER', ' STALLION'], ['BLOCK', ' COVER', ' HIDE', ' MASK', ' CROWN', ' DIAL', ' HAND', ' STRAP', ' LASSO', ' SHIELD', ' SWORD', ' TIARA', ' CANDIDATE', ' FAUCET', ' MASCARA', ' NOSE'], ['ACTION', ' CAMERA', ' CUT', ' LIGHTS', ' CAN', ' COULD', ' MAY', ' MIGHT', ' HEAD', ' LEAD', ' PRIME', ' TOP', ' BUTCHER', ' SCRAP', ' TOILET', ' WAX'], ['GENESIS', ' GERM', ' SEED', ' SOURCE', ' ACTS', ' JOB', ' KINGS', ' MARK', ' FLAMES', ' KRAKEN', ' STARS', ' WILD', ' NAP', ' PLANT', ' RANGER', ' TRIP'], ['CORN', ' CUCUMBER', ' PEPPER', ' TOMATO', ' CROWN', ' DOME', ' MELON', ' NOODLE', ' CUT', ' NUMBER', ' SINGLE', ' TRACK', ' BIRD', ' KETTLE', ' REFEREE', ' TRAIN'], ['ANNIVERSARY', ' BIRTHDAY', ' SHOWER', ' WEDDING', ' BARS', ' RECEPTION', ' SERVICE', ' SIGNAL', ' BATH', ' DERBY', ' READING', ' SANDWICH', ' COMIC', ' MET', ' ROCK', ' SOAP'], ['DARREN', ' KAREN', ' SHARON', ' AARON', ' DALE', ' BROOK', ' SAVANNA', ' CLIFF', ' DREW', ' ROSE', ' WILL', ' MAY', ' EVE', ' HANNAH', ' OTTO', ' NATAN'], ['DEAD', ' HAHA', ' LOL', ' ROFL', ' DADA', ' DECO', ' GOTHIC', ' POP', ' HOOK', ' NANA', ' PETER', ' WENDY', ' BIRD', ' GAGA', ' LUCK', ' MACBETH'], ['ARM', ' BRANCH', ' CHAPTER', ' WING', ' BUSHEL', ' PECK', ' STONE', ' TON', ' ANGEL', ' CUB', ' MET', ' RED', ' AUNT', ' BEATLE', ' FLEE', ' NAT'], ['MISTLETOE', ' REINDEER', ' SNOWMAN', ' STOCKING', ' DISPLAY', ' EXHIBIT', ' PRESENT', ' SHOW', ' BAGEL', ' CHEERIO', ' DONUT', ' LIFESAVER', ' CANDY CANE', ' CROSSWALK', ' REFEREE', ' TIGER'], ['AFGHAN', ' ALPACA', ' ANGORA', ' YAK', ' BLATHER', ' CHAT', ' JABBER', ' GAB', ' CONVERSE', ' JORDAN', ' PUMA', ' VANS', ' LEAD', ' SPEECH', ' TRIAL', ' WATER'], ['BOW', ' KNEEL', ' SALUTE', ' STAND', ' CLOCK', ' MAIL', ' MAPS', ' NOTES', ' DOWN', ' FUR', ' SCALES', ' SHELL', ' ARROW', ' DOG', ' FINGER', ' HINT'], ['CUP', ' LID', ' STIRRER', ' STRAW', ' BAT', ' MOTH', ' OWL', ' WOLF', ' BEET', ' BRICK', ' CARDINAL', ' POPPY', ' ACTION', ' BALLPARK', ' GO', ' STICK'], ['CLUB', ' DIAMOND', ' HEART', ' SPADE', ' IRON', ' PUTTER', ' WEDGE', ' WOOD', ' ACHE', ' LONG', ' PINE', ' THIRST', ' LOW', ' SHORT', ' SHY', ' WANTING'], ['CENTRAL', ' CRITICAL', ' KEY', ' VITAL', ' GLASS', ' METAL', ' PAPER', ' PLASTIC', ' HENRY', ' JENNIFER', ' KATE', ' ROCK', ' ASSIGNMENT', ' DEFEAT', ' TEMPO', ' TIRED'], ['FLASH', ' GLEAM', ' GLITTER', ' SPARKLE', ' FISH', ' FORAGE', ' HUNT', ' TRAP', ' BOUNCE', ' CRUNK', ' DRILL', ' GRIME', ' BEER', ' BULB', ' RAIL', ' YEAR'], ['ACORN', ' CONE', ' POLLEN', ' SAP', ' CHOCOLATE', ' GUM', ' LICORICE', ' LOLLIPOP', ' CHUMP', ' FOOL', ' MARK', ' SUCKER', ' FACE', ' HURRICANE', ' NEEDLE', ' POTATO'], ['BOA', ' MAMBA', ' PYTHON', ' VIPER', ' GARTER', ' SLIP', ' TEDDY', ' THONG', ' ABSTRACT', ' BRIEF', ' DIGEST', ' RUNDOWN', ' CIRCLE', ' HOUSE', ' MONTY', ' MOON'], ['BOUQUET', ' RING', ' TRAIN', ' VEIL', ' CAKE', ' COAT', ' COVER', ' CRUST', ' BLACK', ' FROST', ' MA', ' SPARROW', ' BOOK', ' GRAM', ' IN', ' TUBE'], ['GRATER', ' LADLE', ' PEELER', ' WHISK', ' BIRD', ' FISH', ' MAMMAL', ' REPTILE', ' DINOSAUR', ' MUSHROOM', ' PLUMBER', ' PRINCESS', ' BUNKER', ' CLEAVER', ' PARTRIDGE', ' TANNER'], ['FIT', ' HEALTHY', ' SOUND', ' STRONG', ' DIP', ' DROP', ' FALL', ' SINK', ' FOUNTAIN', ' SPRING', ' TAP', ' WELL', ' KEYS', ' NICKS', ' SUMMER', ' SWIFT'], ['FLOAT', ' MALT', ' SHAKE', ' SUNDAE', ' CONCRETE', ' FIRM', ' SOLID', ' TANGIBLE', ' GLASS', ' OLD', ' SIGNS', ' SPLIT', ' DASH', ' HOVER', ' KEY', ' STAR'], ['BARTENDER', ' CHEF', ' HOST', ' SERVER', ' BUS', ' CAR', ' MOTORCYCLE', ' TRUCK', ' ANIMAL', ' BEAKER', ' GONZO', ' SCOOTER', ' DIGIT', ' DOG', ' MITT', ' PIGGY'], ['BACKUP', ' COPY', ' EXTRA', ' SPARE', ' ALLEY', ' BALL', ' LANE', ' PIN', ' MUG', ' PEN', ' TEE', ' TOTE', ' ATE', ' FOR', ' TOO', ' WON'], ['BOOKMARK', ' HISTORY', ' TAB', ' WINDOW', ' BUTTON', ' COLLAR', ' CUFF', ' POCKET', ' BOND', ' LINK', ' RELATION', ' TIE', ' DOZEN', ' JOKE', ' LAUNDRY', ' MARTINI'], ['BRIGHT', ' CLEVER', ' QUICK', ' SHARP', ' ALASKA', ' FRONTIER', ' SOUTHWEST', ' SPIRIT', ' COWBOY', ' DRIFTER', ' OUTLAW', ' SHERIFF', ' LASSO', ' MARS', ' ROGERS', ' SMART'], ['APRICOT', ' FIG', ' GRAPE', ' LIME', ' DELUXE', ' GRAND', ' LAVISH', ' OPULENT', ' BERRY', ' FOSTER', ' STONE', ' SWANK', ' ENVIOUS', ' FRESH', ' NAIVE', ' UNWELL'], ['GIANT', ' PRINCESS', ' WITCH', ' WOLF', ' BISHOP', ' MATE', ' GAMBIT', ' QUEEN', ' CHARLIE', ' PEPPERMINT PATTY', ' PIGPEN', ' WOODSTOCK', ' LUCY', ' NEW YORK', ' ROCK N ROLL', ' YOU'], ['BUFFALO', ' COW', ' GOAT', ' SHEEP', ' BEAM', ' GLOW', ' RADIATE', ' SHINE', ' FLOOR', ' HORSE', ' RINGS', ' VAULT', ' CUTIE', ' ENVY', ' EXCEL', ' SEEDY'], ['IRIS', ' LENS', ' PUPIL', ' RETINA', ' BOGUS', ' FAKE', ' PHONY', ' SHAM', ' COPY', ' OUT', ' OVER', ' ROGER', ' ALEJANDRO', ' LOLA', ' MICHELLE', ' STAN'], ['GET OUT', ' GO', ' LEAVE', ' SCRAM', ' ME', ' THEM', ' US', ' YOU', ' NOPE', ' OPEN', ' PEON', ' PONE', ' BEANIE', ' FUR', ' NEPO', ' SANTA'], ['CHAI', ' COCOA', ' COFFEE', ' TEA', ' BUZZ', ' CLUCK', ' MEOW', ' OINK', ' BARK', ' BRANCH', ' ROOT', ' TRUNK', ' DIRT', ' DISH', ' SCOOP', ' SKINNY'], ['BAT', ' COBWEB', ' PUMPKIN', ' TOMBSTONE', ' 24', ' BONES', ' FIREFLY', ' WEEDS', ' 7', ' BAR', ' BELL', ' CHERRY', ' 22', ' 451', ' 2001', ' 20', '000'], ['ANACONDA', ' CAPYBARA', ' JAGUAR', ' TOUCAN', ' BASE', ' BOTTOM', ' FOOT', ' FOUNDATION', ' COMPANY', ' GREASE', ' HAIR', ' RENT', ' CHANGE', ' CUCUMBER', ' LEGS', ' LION'], ['BALL', ' OUT', ' SAFE', ' STRIKE', ' FORGE', ' FURNACE', ' KILN', ' OVEN', ' CARP', ' CATFISH', ' FLOUNDER', ' SMELT', ' COLONEL', ' SALMON', ' WALK', ' YOLK'], ['ESSENCE', ' HEART', ' SPIRIT', ' SOUL', ' CIDER', ' PORT', ' SAKE', ' STOUT', ' BRAVE', ' CARS', ' COCO', ' UP', ' DEMO', ' RED', ' SCOTCH', ' TICKER'], ['HORROR', ' PICTURE', ' ROCKY', ' SHOW', ' FRAMED', ' RABBIT', ' ROGER', ' WHO', ' HARRY', ' MET', ' SALLY', ' WHEN', ' FURY', ' MAD', ' MAX', ' ROAD'], ['GNOME', ' GOBLIN', ' OGRE', ' TROLL', ' BUD', ' LEAF', ' PETAL', ' STALK', ' AGENT', ' MOLE', ' PLANT', ' SPY', ' DRAGON', ' HORSE', ' RABBIT', ' TIGER'], ['CHART', ' DIAGRAM', ' GRAPH', ' MAP', ' BONUS', ' EXTRA', ' ICING', ' PERK', ' GRAVY', ' PIE', ' STUFFING', ' TURKEY', ' I RAN', ' ISTANBUL', ' MONTERO', ' SATISFACTION'], ['BRUSH', ' CANVAS', ' EASEL', ' PALETTE', ' DRIVE', ' NEUTRAL', ' PARK', ' REVERSE', ' COMB', ' GEAR', ' SAW', ' ZIPPER', ' FIRST', ' FOLDING', ' HIGH', ' LAWN'], ['COW', ' DOE', ' HEN', ' MARE', ' I', ' IT', ' THEY', ' WE', ' D', ' L', ' M', ' V', ' EWE', ' U', ' YEW', ' YOU'], ['BARE', ' NAKED', ' NUDE', ' UNCLAD', ' BUN', ' DANISH', ' MUFFIN', ' TURNOVER', ' FUMBLE', ' PUNT', ' SACK', ' SNAP', ' BUFF', ' CLIP', ' FILE', ' POLISH'], ['GOBLET', ' SNIFTER', ' TUMBLER', ' STEIN', ' CLARINET', ' FLUTE', ' OBOE', ' SAXOPHONE', ' BISHOP', ' FROST', ' OLDS', ' POUND', ' BALLOON', ' BASSOON', ' COFFEE', ' FRICASSEE'], ['FRY', ' NACHO', ' POPPER', ' WING', ' BINGO', ' CORRECT', ' RIGHT', ' YES', ' CHIP', ' DING', ' NICK', ' SCRATCH', ' APPLE', ' CRACKER', ' FLAP', ' LUMBER'], ['SANDBOX', ' SEESAW', ' SLIDE', ' SWING', ' CLOUT', ' PULL', ' SWAY', ' WEIGHT', ' ANKH', ' CROOK', ' EYE', ' SCARAB', ' COURIER', ' IMPACT', ' PAPYRUS', ' TIMES'], ['BOOK', ' BOUNCE', ' RUN', ' SPLIT', ' FOX', ' IBEX', ' LYNX', ' ORYX', ' EBONY', ' JET', ' ONYX', ' RAVEN', ' ASH', ' BLACK', ' CYBER', ' FAT'], ['BLISS', ' CLOUD NINE', ' HEAVEN', ' PARADISE', ' CON', ' FAST ONE', ' HUSTLE', ' RACKET', ' HIGH FIVE', ' HUG', ' SHAKE', ' WAVE', ' BUCKET', ' GUEST', ' TOP TEN', ' WISH'], ['BREAST', ' DRUMSTICK', ' TENDER', ' WING', ' DRIVER', ' EAGLE', ' HOLE', ' STROKE', ' CYMBAL', ' KICK', ' SNARE', ' TOM', ' INFANT', ' PUB', ' SWIMMING', ' TICKER'], ['RISK', ' SORRY', ' TABOO', ' TROUBLE', ' BUSINESS', ' NATIONAL', ' OPINION', ' STYLE', ' ATLAS', ' HERMES', ' NIKE', ' PARIS', ' FOXY', ' GUCCI', ' KILLER', ' NOTORIOUS'], ['BASH', ' BLOWOUT', ' PARTY', ' SHINDIG', ' CRICKET', ' PUPPET', ' WHALE', ' WOODCARVER', ' COUNTER', ' MIXER', ' RANGE', ' SINK', ' BUNNY', ' EGG', ' ISLAND', ' SUNDAY'], ['DODO', ' MAMMOTH', ' MASTODON', ' TRILOBITE', ' BUSTS', ' FLOPS', ' MISSES', ' TURKEYS', ' DUDS', ' GETUP', ' OUTFIT', ' THREADS', ' PECK', ' SMACK', ' SMOOCH', ' X'], ['BEARD', ' GOATEE', ' MUSTACHE', ' STUBBLE', ' GEAR', ' HANDLEBAR', ' PEDAL', ' WHEEL', ' DOG', ' FOLLOW', ' TAIL', ' TRACK', ' DOUBT', ' MOVIE', ' SHADOW', ' VOTE'], ['ACTOR', ' DANCER', ' SINGER', ' STAND-UP', ' COMET', ' CUPID', ' DASHER', ' VIXEN', ' CARD', ' CHOCOLATE', ' HEART', ' ROSE', ' BOYS', ' LIEUTENANT', ' SANTA', ' TASTE'], ['ARIZONA', ' COLORADO', ' NEVADA', ' UTAH', ' CRUSH', ' MUG', ' SPRITE', ' SQUIRT', ' GENESIS', ' KANSAS', ' RUSH', ' YES', ' HAWK', ' MONTANA', ' SOPRANO', ' STARK'], ['COOLER', ' LANTERN', ' SLEEPING BAG', ' TENT', ' BARB', ' DIG', ' DISS', ' JAB', ' MINUTE', ' SLIGHT', ' SMALL', ' WEE', ' CAMPER', ' HOUR', ' MEAL', ' MEDIUM'], ['BUD', ' CHUM', ' MATE', ' PAL', ' CROCK', ' POT', ' SKILLET', ' WOK', ' CLOG', ' PUMP', ' SLIDE', ' WEDGE', ' GRASS', ' HERB', ' MARY JANE', ' WEED']]

@app.route("/play")

def play():
    global index
    global x
    global sample
    x = random.choice(lst)

    #getting the game number
    index = lst.index(x) + 4

    # print(x)
    # print(x[0:4])
    # print(sorted(x[0:4]))
    # print(len(x), "thid is lenx")
    sample = random.sample(x, len(x))
    one = sample[0]
    two = sample[1]
    three = sample[2]
    four = sample[3]
    five = sample[4]
    six = sample[5]
    seven = sample[6]
    eight = sample[7]
    nine = sample[8]
    ten = sample[9]
    eleven = sample[10]
    twelve = sample[11]
    thirteen = sample[12]
    fourteen = sample[13]
    fifteen = sample[14]
    sixteen = sample[15]
    
    return render_template('hi.html', one=one, two=two, three=three, four=four, five=five, six=six, seven=seven, eight=eight, nine=nine, ten=ten, eleven=eleven, twelve=twelve, thirteen=thirteen, fourteen=fourteen, fifteen=fifteen, sixteen=sixteen, index=index)

@app.route('/submit', methods=['POST'])
def my_form_post():
    global count
    global x
    global sample
    score = 0
    categories = 0 
    tname = request.form.get('name')
    if tname:
        name = tname
    else:
        name = "hi"
    #print(request.method, "method")

    dict = {}
    dict[1] = request.form.get('v1')
    dict[2] = request.form.get('v2')
    dict[3] = request.form.get('v3')
    dict[4] = request.form.get('v4')
    dict[5] = request.form.get('v5')
    dict[6] = request.form.get('v6')
    dict[7] = request.form.get('v7')
    dict[8] = request.form.get('v8')
    dict[9] = request.form.get('v9')
    dict[10] = request.form.get('v10')
    dict[11] = request.form.get('v11')
    dict[12] = request.form.get('v12')
    dict[13] = request.form.get('v13')
    dict[14] = request.form.get('v14')
    dict[15] = request.form.get('v15')
    dict[16] = request.form.get('v16')

    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    print(dict, "dict")
    print(sample, "sample")
    for a, y in dict.items():
        print(a, y, "this is ay")
        a = a-1
        if y == "Group 1":
            arr1.append(sample[a])
        if y == "Group 2":
            arr2.append(sample[a])
        if y == "Group 3":
            arr3.append(sample[a])
        if y == "Group 4":
            print("hi")
            arr4.append(sample[a])
    
    ans = [sorted(x[4:8]), sorted(x[8:12]), sorted(x[12:16]), sorted(x[0:4])]
    #print(arr1, arr2, arr3, arr4, "arrs")
    #print(ans, "ans")

    # computing total score + category score
    if sorted(arr1) in ans:
        score+=1
        categories +=1
        if sorted(arr1) == sorted(x[4:8]):
            score += 1
        if sorted(arr1) == sorted(x[8:12]):
            score += 2
        if sorted(arr1) == sorted(x[12:16]):
            score += 3
    if sorted(arr2) in ans:
        score+=1
        categories +=1
        if sorted(arr2) == sorted(x[4:8]):
            score += 1
        if sorted(arr2) == sorted(x[8:12]):
            score += 2
        if sorted(arr2) == sorted(x[12:16]):
            score += 3
    if sorted(arr3) in ans:
        score+=1
        categories +=1
        if sorted(arr3) == sorted(x[4:8]):
            score += 1
        if sorted(arr3) == sorted(x[8:12]):
            score += 2
        if sorted(arr3) == sorted(x[12:16]):
            score += 3
    if sorted(arr4) in ans:
        score+=1
        categories +=1
        if sorted(arr4) == sorted(x[4:8]):
            score += 1
        if sorted(arr4) == sorted(x[8:12]):
            score += 2
        if sorted(arr4) == sorted(x[12:16]):
            score += 3
    res = str([arr1, arr2, arr3, arr4])
    #print(score)
    p = Profile(name=name, score=score, catnum=categories, gamenum=index, num=datetime.now(), result=res)
    db.session.add(p)
    db.session.commit()
    #profs.append(p)
    return redirect('/play')

@app.route('/view')
def index():
    #print(profs)
    # for p in profs:
    #     print(p)
        
    # profs.clear()
    profiles = Profile.query.all()
    return render_template('view.html', profiles=profiles)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
