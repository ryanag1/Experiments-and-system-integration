<template>
    <v-app>
        <app-bar
            :duct="duct"
            @drawer-icon-click="toggleMenuDrawer"
        >
        </app-bar>

        <menu-drawer :drawer="menuDrawer"></menu-drawer>

        <keep-alive>
            <router-view app
                v-if="duct"
                :duct="duct"
                ref="child"
            ></router-view>
        </keep-alive>

    </v-app>
</template>

<script>
import myapp from '@/lib/myapp.js'
import AppBar from '@/components/views/ConsoleAppBar'
import MenuDrawer from '@/components/views/ConsoleMenuDrawer'

export default {
    components: { 
        AppBar,
        MenuDrawer
    },
    //props: ["duct"],
    data: () => ({
        duct: null,
        wsdPath: "/ducts/wsd",
        menuDrawer: false
    }),

    created: function(){
      this.duct = new myapp.Duct();
      this.duct.logger = new myapp.DuctEventLogger(this.duct);
      this.duct.open(this.wsdPath);

      console.log(sessionStorage.getItem("Auth"));

      this.duct.invokeOrWaitForOpen(() => {
        this.duct.eventListeners.resource.on("createSession", {
          success: (data) => {
            console.log(data);
            if(!data["Auth"]) {
              sessionStorage.removeItem("Auth");
              localStorage.removeItem("userId");
              localStorage.removeItem("clientToken");
              window.location.href = `./login`;
            }
          },
          error: (data) => {
            console.log(data);
          }
        })
        this.clientToken = localStorage.getItem("clientToken");
        this.userId = localStorage.getItem("userId");
        this.duct.controllers.resource.createSession(this.userId, this.clientToken);
      })

    },

    methods: {
      toggleMenuDrawer() { this.menuDrawer = !this.menuDrawer; },
      loadClientToken() {
        return new Promise((resolve, reject) => {
          this.clientToken = localStorage.getItem("clientToken");
                this.userId = localStorage.getItem("userId");
                if(this.clientToken) resolve();
                else reject();
            });
      },
    }
}
</script>
<style>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.5s;
  transition-property: opacity;
  transition-timing-function: ease-in;
}

.fade-enter-active {
  transition-duration: 0.5s;
}

.fade-enter,
.fade-leave-active {
  opacity: 0
}

.vjs-tree {
    font-size: 10px;
}
</style>
