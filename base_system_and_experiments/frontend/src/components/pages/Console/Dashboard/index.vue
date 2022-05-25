<template>
  <v-main class="mt-10 grey lighten-4">
    <v-card
      max-width="450"
      class="mx-auto"
    >
      <v-toolbar
        color="cyan"
        dark
      >
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title>Inbox</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </v-toolbar>

      <v-list three-line>
        <template v-for="(item, index) in items">
          <v-subheader
            v-if="item.header"
            :key="item.header"
            v-text="item.header"
          ></v-subheader>

          <v-divider
            v-else-if="item.divider"
            :key="index"
            :inset="item.inset"
          ></v-divider>

          <v-list-item
            v-else
            :key="item.title"
          >
            <v-list-item-avatar color="cyan">
              <span class="white--text text-h5">{{ item.initial }}</span>
            </v-list-item-avatar>

            <v-list-item-content>
                <v-list-item-title v-html="item.title"></v-list-item-title>
                <v-list-item-subtitle v-html="item.subtitle"></v-list-item-subtitle>
                <v-textarea v-if="item.title == userId" :key="userId" solo name="input-7-4" label="Solo textarea" readonly v-model="recievedMsg" ></v-textarea>
                <v-textarea v-else :key="item.title" solo name="input-7-4" label="Solo textarea"  v-model="item.msg" ></v-textarea>
            </v-list-item-content>

            <v-list-item-action>
              <v-btn icon>
                <v-icon color="grey lighten-1" :disabled="item.title == userId" @click="opponentId=item.title; $refs.dlgCall.show=true; onOpenCalling();/*sendData(item.title, item.msg)*/">mdi-phone-outgoing</v-icon>
              </v-btn>
            </v-list-item-action>
            <v-list-item-action>
              <v-btn icon>
                <v-icon color="grey lighten-1" @click="/*fetchMsgData()*/">mdi-phone-incoming</v-icon>
              </v-btn>
            </v-list-item-action>

          </v-list-item>
        </template>
      </v-list>

      <!--<div id="media" style="display: block">
          <audio id="audio" autoplay="true"></audio>
          <video id="video" autoplay="true" playsinline="true"></video>
      </div>-->
    </v-card>

    <dialog-call :duct="duct" :pc="pc" :opponentId="opponentId" :fetchData="fetchData" :sender="sender" :reciever="reciever" :userId="userId" v-on:sr-change="onSRChange" ref="dlgCall"></dialog-call>

  </v-main>
</template>

<script>
/* eslint-disable no-inner-declarations */
  export default {
    props: ["duct"],
    components: {
      DialogCall: () => import("./DialogCall")
    },
    data: () => ({
      pc: null,
      dc: null,
      iceGatheringLog: "",
      iceConnectionLog: "",
      signalingLog: "",
      sender: false,
      reciever: false,
      userId: null,
      recievedMsg: null,
      items: [
        /*{ header: 'Today' },
        {
          avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
          title: 'Brunch this weekend?',
          subtitle: `<span class="text--primary">Ali Connors</span> &mdash; I'll be in your neighborhood doing errands this weekend. Do you want to hang out?`,
        },
        { divider: true, inset: true },
        {
          avatar: 'https://cdn.vuetifyjs.com/images/lists/2.jpg',
          title: 'Summer BBQ <span class="grey--text text--lighten-1">4</span>',
          subtitle: `<span class="text--primary">to Alex, Scott, Jennifer</span> &mdash; Wish I could come, but I'm out of town this weekend.`,
        },
        { divider: true, inset: true },
        {
          avatar: 'https://cdn.vuetifyjs.com/images/lists/3.jpg',
          title: 'Oui oui',
          subtitle: '<span class="text--primary">Sandra Adams</span> &mdash; Do you have Paris recommendations? Have you ever been?',
        },*/
      ],
      opponentId: null,
      fetchData: null
    }),
    watch: {
      /*iceGatheringLog() {

        console.log("iceGatheringLog");
        console.log(this.iceGatheringLog);
      },
      iceConnectionLog() {
        console.log("iceConnectionLog");
        console.log(this.iceConnectionLog);
      },
      signalingLog() {
        console.log("signalingLog");
        console.log(this.signalingLog);
      }*/
    },
    created: function() {

      this.duct.controllers.resource.fetchDataFromSpecificUser(localStorage.getItem("userId"), localStorage.getItem("clientToken"));

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


      //let utf8decoder = new TextDecoder();
      this.userId = localStorage.getItem("userId");
      this.duct.invokeOrWaitForOpen(() => {
        this.duct.eventListeners.resource.on("fetchAllActive", {
          success: (data) => {
            //console.log(data);
            //console.log(utf8decoder.decode(data["ActiveUserIds"][0][0]));
            this.items.push( { header: 'Today' } );
            for( let i in data["ActiveUserIds"] ) {
              this.items.push( {
                initial: data["ActiveUserIds"][i][0],
                title: data["ActiveUserIds"][i],
                subtitle: `<span class="text--primary">Ali Connors</span> &mdash; I'll be in your neighborhood doing errands this weekend. Do you want to hang out?`,
                msg: null
              } );
            }
          },
          error: (data) => {
            console.log(data);
          }
        });
        /*this.duct.eventListeners.resource.on("addDataForSpecificUser", {
          success: (data) => {
            console.log("storedData");
            console.log(data);
            if(!this.reciever) {
              this.sender = true;
            }
            //console.log(utf8decoder.decode(data["ActiveUserIds"][0][0]));
          },
          error: (data) => {
            console.log(data);
          }
        });*/
        //Undo this comment out
        /*this.duct.eventListeners.resource.on("fetchDataFromSpecificUser", {
          success: (data) => {
            console.log(data);
            this.recievedMsg = data["Message"];
            let toUserId = data["FromUserId"];
            if(!this.sender) {
              this.reciever = true;
            }
            console.log("JSON.parse(this.recievedMsg)");
            console.log(JSON.parse(this.recievedMsg));
            this.pc.setRemoteDescription(JSON.parse(this.recievedMsg));

            if(this.reciever) {
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
            }

            //console.log(utf8decoder.decode(data["ActiveUserIds"][0][0]));
          },
          error: (data) => {
            console.log(data);
          }
        });*/
        //Comment out this 
        this.duct.eventListeners.resource.on("fetchDataFromSpecificUser", {
          success: (data) => {
            if(data["Message"] == "{token:'terminate'}") {
              console.log("terminate1");
            }
            else {
              console.log(data);
              //this.recievedMsg = data["Message"];
              //let toUserId = data["FromUserId"];
              if(!this.sender) {
                this.reciever = true;
                this.onOpenCalling();
                this.$refs.dlgCall.show=true
              }
              this.duct.controllers.resource.fetchDataFromSpecificUser(localStorage.getItem("userId"), localStorage.getItem("clientToken"));
              this.fetchData = data;
            }
          },
          error: (data) => {
            console.log(data);
          }
        });
      });
     
      this.duct.controllers.resource.fetchAllActive(localStorage.getItem("userId"), localStorage.getItem("clientToken"));

      /*console.log(navigator);
      //this.getMediaStream();
      
      navigator.mediaDevices.getUserMedia({ video: false, audio: true }).then(function(stream) {
        stream.getTracks().forEach(function(track) {
            self.pc.addTrack(track, stream);
        });
        }, function(err) {
            alert('Could not acquire media: ' + err);
      });*/

    },
    methods: {
      onOpenCalling() {
        let self = this;
        const config = {
          "iceServers": [
              { "urls": "stun:stun.l.google.com:19302" },
              //{ "urls": "stun:stun1.l.google.com:19302" },
              //{ "urls": "stun:stun2.l.google.com:19302" },
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

        /*this.pc.addEventListener('track', function(evt) {
          if (evt.track.kind == 'video')
              document.getElementById('video').srcObject = evt.streams[0];
          else
              document.getElementById('audio').srcObject = evt.streams[0];
        });*/
        navigator.mediaDevices.getUserMedia({ video: {
            width: {
                min: 320,
                max: 1280
            },height: {
                min: 240,
                max: 720
            },frameRate: {
                min: 1,
                max: 10
            }
          }, audio: true }).then(function(stream) {
            stream.getTracks().forEach(function(track) {
                self.pc.addTrack(track, stream);
            });
            }, function(err) {
                alert('Could not acquire media: ' + err);
        });
      },

      async getMediaStream() {
        let that = this;
        const localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localStream.getTracks().forEach(function(track) {
            that.pc.addTrack(track, localStream);
        });
      },
      sendData(toUserId, msg) {
        let self = this;
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
          self.duct.controllers.resource.addDataForSpecificUser(toUserId, self.userId, JSON.stringify(offer));
        });
        console.log(msg);
        //console.log(offer);
        //this.duct.controllers.resource.addDataForSpecificUser(toUserId, this.userId, offer);
      },
      fetchMsgData() {
        console.log(this.signalingLog);
        this.duct.controllers.resource.fetchDataFromSpecificUser(localStorage.getItem("userId"), localStorage.getItem("clientToken"));
      },
      onSRChange(e) {
        console.log("SRChange");
        this.sender = e["sender"];
        this.reciever = e["reciever"];
      }
    },
    beforeDestroy() {
      console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
      this.duct.controllers.resource.addDataForSpecificUser(this.userId, this.userId, "{token:'terminate'}");
    },
  }
/* eslint-disable no-inner-declarations */
</script>