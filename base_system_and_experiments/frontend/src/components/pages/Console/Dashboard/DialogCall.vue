<template>
    <v-dialog v-model="show" max-width="1400" fullscreen persistent>
        <v-card>
            <v-card-title class="headline">
                <v-icon class="mr-2" color="indigo">mdi-database-check</v-icon>
                Call to ...
                <v-spacer/>
                <!--<v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details />-->
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col class="text-right">
                            <v-btn icon>
                                <v-icon>mdi-monitor-off</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col class="text-center">
                            <div id="media" style="display: block">
                                <audio id="audio" autoplay="true"></audio>
                                <video id="video" autoplay="true" playsinline="true"></video>
                            </div>
                        </v-col>
                    </v-row>
                </v-container>

            </v-card-text>
            
            <v-card-actions>
                
                <v-spacer></v-spacer>
                <!--<span class="group mx-2 teal">-->
                <v-btn 
                    class="mr-6"
                    fab
                    dark
                    color="primary"
                    @click="startCalling"
                >
                    <v-icon>mdi-phone-in-talk</v-icon>
                </v-btn>
                <v-btn 
                    class="ml-6"
                    fab
                    dark
                    color="pink"
                    @click="closeDialog"
                >
                    <v-icon>mdi-phone-off</v-icon>
                </v-btn>
                <!--</span>-->
                <v-spacer></v-spacer>

                <!--<v-btn text @click="closeDialog" >Close</v-btn>-->
            </v-card-actions>
        </v-card>

        
    </v-dialog>
</template>

<script>
/* eslint-disable no-inner-declarations */
export default {
    data: () => ({
        show: false,
        //pc: null,
        dc: null,
        iceGatheringLog: "",
        iceConnectionLog: "",
        signalingLog: "",
        recievedMsg: null,
        toUserId: null,
        time_start: null,
        dcInterval: null
        //search: ""
    }),
    props: ["duct", "opponentId", "fetchData", "sender", "reciever", "userId", "pc"],
    created: function(){
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("addDataForSpecificUser", {
                success: (data) => {
                    console.log("storedData");
                    console.log(data);
                    //if(!this.reciever) {
                        //this.sender = true;
                        //const args = { "sender": true, "reciever": false };
                        //this.$emit("sr-change", args);
                    //}
                    //console.log(utf8decoder.decode(data["ActiveUserIds"][0][0]));
                },
                error: (data) => {
                    console.log(data);
                }
            });
        });

        /*let self = this;
        const config = {
            "iceServers": [
                { "urls": "stun:stun.l.google.com:19302" },
                { "urls": "stun:stun1.l.google.com:19302" },
                { "urls": "stun:stun2.l.google.com:19302" },
            ]
        }
        this.pc = new RTCPeerConnection(config);

        // register some listeners to help debugging
        this.pc.addEventListener('icegatheringstatechange', function() {
            self.iceGatheringLog += ' -> ' + self.pc.iceGatheringState;
            console.log(self.iceGatheringLog);
        }, false);
        this.iceGatheringLog = this.pc.iceGatheringState;

        this.pc.addEventListener('iceconnectionstatechange', function() {
            self.iceConnectionLog += ' -> ' + self.pc.iceConnectionState;
            console.log(self.iceConnectionLog);
        }, false);
        this.iceConnectionLog = this.pc.iceConnectionState;

        this.pc.addEventListener('signalingstatechange', function() {
            self.signalingLog += ' -> ' + self.pc.signalingState;
            console.log(self.signalingLog);
        }, false);
        this.signalingLog = this.pc.signalingState;

        this.pc.addEventListener('track', function(evt) {
            if (evt.track.kind == 'video')
                document.getElementById('video').srcObject = evt.streams[0];
            else
                document.getElementById('audio').srcObject = evt.streams[0];
        });*/

        //console.log(navigator);
        //this.getMediaStream();
        
        /*navigator.mediaDevices.getUserMedia({ video: false, audio: true }).then(function(stream) {
            stream.getTracks().forEach(function(track) {
                self.pc.addTrack(track, stream);
            });
            }, function(err) {
                alert('Could not acquire media: ' + err);
        });*/

    },
    components: {
        
    },
    computed: {
        
    },
    methods: {
        current_stamp() {
            if (this.time_start === null) {
                this.time_start = new Date().getTime();
                return 0;
            } else {
                return new Date().getTime() - this.time_start;
            }
        },
        closeDialog() {
            this.pc.close();
            const args = { "sender": false, "reciever": false };
            this.$emit("sr-change", args);
            this.duct.controllers.resource.addDataForSpecificUser(localStorage.getItem("userId"), localStorage.getItem("userId"), "{token:'terminate'}");
            this.duct.controllers.resource.fetchDataFromSpecificUser(localStorage.getItem("userId"), localStorage.getItem("clientToken"));
            this.show = false;
        },
        startCalling() {
            let self = this;
            this.time_start = null;
            this.dc = this.pc.createDataChannel('chat', {"ordered":true});
            this.dc.onclose = function() {
                clearInterval(this.dcInterval);
                console.log('- close');
            };
            this.dc.onopen = function() {
                //var self = this;
                console.log('- open');
                this.dcInterval = setInterval(function() {
                    var message = 'ping ' + self.current_stamp();
                    console.log('> ' + message);
                    self.dc.send(message);
                }, 1000);
            };
            this.dc.onmessage = function(evt) {
                //var self = this;
                console.log('< ' + evt.data);

                if (evt.data.substring(0, 4) === 'pong') {
                    var elapsed_ms = self.current_stamp() - parseInt(evt.data.substring(5), 10);
                    console.log(' RTT ' + elapsed_ms + ' ms');
                }
            };

            this.pc.addEventListener('track', function(evt) {
                if (evt.track.kind == 'video') {
                    document.getElementById('video').srcObject = evt.streams[0];
                }
                else{
                    document.getElementById('audio').srcObject = evt.streams[0];
                }
            });

            if(this.reciever) {
                //let self = this;
                console.log("answer");
                this.pc.createAnswer().then((answer) => {
                    console.log(answer);
                    //console.log(JSON.stringify(offer));
                    //console.log(typeof answer);
                    return self.pc.setLocalDescription(answer);
                }).then(function() {
                    var answer = self.pc.localDescription;
                    
                    self.duct.controllers.resource.addDataForSpecificUser(self.toUserId, self.userId, JSON.stringify(answer));
                });
            } else {

                if(!this.reciever) {
                    //this.sender = true;
                    const args = { "sender": true, "reciever": false };
                    this.$emit("sr-change", args);
                }

                console.log(this.opponentId);
                //this.duct.controllers.resource.addDataForSpecificUser(this.opponentId, localStorage.getItem("userId"), "{MSG:'JSON.stringify(offer)'}");
                
                //let self = this;
                this.pc.createOffer().then((offer) => {
                console.log("offer");
                console.log(offer);
                //console.log(JSON.stringify(offer));
                //console.log(typeof offer);
                return self.pc.setLocalDescription(offer);

                //console.log(typeof JSON.stringify(offer));
                //this.duct.controllers.resource.addDataForSpecificUser(toUserId, this.userId, JSON.stringify(offer));
                }).then(function() {
                    // wait for ICE gathering to complete
                    return new Promise(function(resolve) {
                        if (self.pc.iceGatheringState === 'complete') {
                            resolve();
                        } else {
                            function checkState() {
                                if (self.pc.iceGatheringState === 'complete') {
                                    self.pc.removeEventListener('icegatheringstatechange', checkState);
                                    resolve();
                                }
                            }
                            self.pc.addEventListener('icegatheringstatechange', checkState);
                        }
                    });
                }).then(function() {
                    var offer = self.pc.localDescription;
                    self.duct.controllers.resource.addDataForSpecificUser(self.opponentId, self.userId, JSON.stringify(offer));
                });
            }
        }
    },
    watch: {
        fetchData() {
            console.log(this.fetchData);
            if(this.fetchData["Message"] == "{token:'terminate'}") {
              console.log("terminate2");
            }
            else {
                //let self = this;
                this.recievedMsg = this.fetchData["Message"];
                this.toUserId = this.fetchData["FromUserId"];
                if(!this.sender) {
                    //this.reciever = true;
                }
                console.log(this.recievedMsg);
                console.log(JSON.parse(this.recievedMsg));
                this.pc.setRemoteDescription(JSON.parse(this.recievedMsg));

                /*if(this.reciever) {
                    console.log("answer");
                    this.pc.createAnswer().then((answer) => {
                        console.log(answer);
                        //console.log(JSON.stringify(offer));
                        //console.log(typeof answer);
                        return self.pc.setLocalDescription(answer);
                    }).then(function() {
                        var answer = self.pc.localDescription;
                        
                        self.duct.controllers.resource.addDataForSpecificUser(toUserId, self.userId, JSON.stringify(answer));
                    });
                }*/

            }
        }
    }
}
/* eslint-disable no-inner-declarations */
</script>
