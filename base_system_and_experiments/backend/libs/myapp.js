window.ducts.myapp = window.ducts.myapp || {};
window.ducts.myapp.event = window.ducts.myapp.event || {};
window.ducts.myapp._local = window.ducts.myapp._local || {};

window.ducts.myapp.Duct = class extends window.ducts.Duct {

    constructor() {
	    super();

        this.onOpenHandlers = [];

        this.controllers = {
            resource: new window.ducts.myapp.ResourceController(this),
            mturk: new window.ducts.myapp.MTurkController(this)
        };
        this.eventListeners = {
            resource: new window.ducts.myapp.ResourceEventListener(),
            mturk: new window.ducts.myapp.MTurkEventListener()
        };

        this.send = 
            (rid, eid, data) => {
                if(this.logger) this.logger.addSent(rid, eid, data);
                return super._send(this, rid, eid, data);
            }

        this.addOnOpenHandler = (handler) => { this.onOpenHandlers.push(handler); };
    }

    _onopen(self, event) {
	    super._onopen( self, event );
        //self.setEventHandler( self.EVENT.APP_WSD, (rid, eid, data) => { self.APP_WSD = data } );
	    //self.send( self.next_rid(), self.EVENT.APP_WSD, null );

        this.setupHandlers(this);
        for(const handler of this.onOpenHandlers)  handler();
    }

    _onmessage(self, event) {
        const [rid, eid, data] = self.decode(MessagePack.Buffer.from(event.source.data));
        if(self.logger) self.logger.addReceived(rid, eid, data);
        super._onmessage( self, event );
    }

    invokeOrWaitForOpen(f) {
        if(this.state==window.ducts.State.OPEN_CONNECTED) f();
        else this.addOnOpenHandler(f);
    }
 
    // FIXME:: needs a protocol
    _handleMTurk(self, name, data) {
        if(data["Status"]=="Success") {
            for(const func of self.eventListeners.mturk[name].success)  func(data["Contents"]);
        } else {
            for(const func of self.eventListeners.mturk[name].error)  func(data);
        }
    }

    _handleResource(self, name, data) {
        if(data["Status"]=="Success")
            for(const func of self.eventListeners.resource[name].success)  func(data["Contents"]);
        else
            for(const func of self.eventListeners.resource[name].error)  func(data);
    }

    setupHandlers(self) {
        
        self.setEventHandler( self.EVENT.CREATE_SESSION,
                              (rid, eid, data) => { self._handleResource(self, "createSession", data); } );
        self.setEventHandler( self.EVENT.LOGIN_FIRST_PAGE,
                              (rid, eid, data) => { self._handleResource(self, "loginFirstPage", data); } );
        self.setEventHandler( self.EVENT.FETCH_ALL_ACTIVE,
                              (rid, eid, data) => { self._handleResource(self, "fetchAllActive", data); } );
        self.setEventHandler( self.EVENT.ADD_DATA_FOR_SPECIFIC_USER,
                              (rid, eid, data) => { self._handleResource(self, "addDataForSpecificUser", data); } );
        self.setEventHandler( self.EVENT.FETCH_DATA_FROM_SPECIFIC_USER,
                              (rid, eid, data) => { self._handleResource(self, "fetchDataFromSpecificUser", data); } );
        self.setEventHandler( self.EVENT.MEDIA_TRANSFORM,
                              (rid, eid, data) => { self._handleResource(self, "mediaTransform", data); } );
        self.setEventHandler( self.EVENT.PING_PONG,
                              (rid, eid, data) => { self._handleResource(self, "pingPong", data); } );
        self.setEventHandler( self.EVENT.CSV_WRITER,
                              (rid, eid, data) => { self._handleResource(self, "csvWriter", data); } );
        self.setEventHandler( self.EVENT.GET_REDIS_TABLE,
                              (rid, eid, data) => { self._handleResource(self, "getRedisTable", data); } );
        self.setEventHandler( self.EVENT.RUN_SCRAPE,
                              (rid, eid, data) => { self._handleResource(self, "runScrape", data); } );
        self.setEventHandler( self.EVENT.TEST_JSON_SERVER,
                              (rid, eid, data) => { self._handleResource(self, "testJsonServer", data); } );
        self.setEventHandler( self.EVENT.ACK_COORDINATE,
                              (rid, eid, data) => { self._handleResource(self, "ackCoordinate", data); } );
    }
};

window.ducts.myapp.DuctEventLogger = class {
    constructor(duct, dataSizeLimit) {
        this._duct = duct;
        this.log = [];
        this.dataSizeLimit = dataSizeLimit || 3000;
    }

    addSent(rid, eid, data) {
        this.log[rid] = { eid, sent: this._skipLargeData(data), received: [] };
    }

    addReceived(rid, eid, data) {
        if(!(rid in this.log))  throw new ReferenceError(`request id ${rid} (eid: ${eid}) is not found in the log`);
        if(this.log[rid].eid != eid)  throw new ReferenceError(`event id ${eid} does not correspond to the log`);

        data["Contents"] = this._skipLargeData(data["Contents"]);
        this.log[rid].received.push(data);
    }

    _skipLargeData(data) {
        var newData = {}
        for(const key in data) {
            if(typeof data[key] === 'object')
                newData[key] = (JSON.stringify(data[key]).length <= this.dataSizeLimit) ? data[key] : "[log skipped]";
        }
        return newData;
    }
}

window.ducts.myapp.DuctEventListener = class extends window.ducts.DuctEventListener {
    constructor() {
        super();
	    this.on =
	        (names, { success, error }) => {
	    	        for(let name of (names instanceof Array) ? names : [names]) {
	    	            if (!(name in this)) {
	    	        	    throw new ReferenceError('['+name+'] is not defined');
	    	            } 

                        // if the listener is an empty object (= no handler is registered yet), then initialize it
                        if(this[name] && Object.keys(this[name]).length === 0 && this[name].constructor === Object)  this[name] = { success: [], error: [] };
                        
	    	            this[name].success.push(success);
	    	            this[name].error.push(error);
	    	        }
            }
    }
};

window.ducts.myapp.ResourceEventListener = class extends window.ducts.myapp.DuctEventListener {
    constructor() {
        super();
        this.createSession = {}
        this.loginFirstPage = {}
        this.fetchAllActive = {}
        this.addDataForSpecificUser = {}
        this.fetchDataFromSpecificUser = {}
        this.mediaTransform = {}
        this.pingPong = {}
        this.csvWriter = {}
        this.getRedisTable = {}
        this.runScrape = {}
        this.testJsonServer = {}
        this.ackCoordinate = {}
    }
}

window.ducts.myapp.MTurkEventListener = class extends window.ducts.myapp.DuctEventListener {
    constructor() {
        super();

    }
}

window.ducts.myapp.MTurkController = class {
    constructor( duct ){
        this._duct = duct;
    }
}

window.ducts.myapp.ResourceController = class {
    constructor(duct){
        this._duct = duct;

        
        this.createSession =
            ( UserId, ClientToken ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.CREATE_SESSION, { UserId, ClientToken } );
            };
        this.loginFirstPage =
            ( Username, Password ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.LOGIN_FIRST_PAGE, { Username, Password } );
            };
        this.fetchAllActive =
            ( UserId, ClientToken ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.FETCH_ALL_ACTIVE, { UserId, ClientToken } );
            };
        this.addDataForSpecificUser =
            (ToUserId, FromUserId, Message) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.ADD_DATA_FOR_SPECIFIC_USER, { ToUserId, FromUserId, Message } );
            }; 
        this.fetchDataFromSpecificUser =
            (UserId, ClientToken) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.FETCH_DATA_FROM_SPECIFIC_USER, { UserId, ClientToken } );
            }; 
        this.mediaTransform =
            (track) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MEDIA_TRANSFORM, { track } );
            }; 
        this.pingPong =
            (obj) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.PING_PONG, { obj } );
            }; 
        this.csvWriter =
            (obj) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.CSV_WRITER, { obj } );
            }; 
        this.getRedisTable =
            (obj) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.GET_REDIS_TABLE, { obj } );
            }; 
        this.runScrape =
            (obj) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.RUN_SCRAPE, { obj } );
            }; 
        this.testJsonServer =
            (obj) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.TEST_JSON_SERVER, { obj } );
            }; 
        this.ackCoordinate = 
        (floatArray, str, num, user_num, intArray) => {
            return this._duct.send( this._duct.next_rid(), this._duct.EVENT.ACK_COORDINATE, this._data({ floatArray, str, num, user_num, intArray }) );
        };
                
    }
    
}
