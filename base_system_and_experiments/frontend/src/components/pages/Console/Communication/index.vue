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

  </v-main>
</template>

<script>
/* eslint-disable no-inner-declarations */
  export default {
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
        { header: 'Today' },
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
        },
      ],
      opponentId: null,
      fetchData: null
    }),
  }
</script>