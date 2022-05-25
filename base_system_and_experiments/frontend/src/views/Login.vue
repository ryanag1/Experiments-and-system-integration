<template>
<v-app>
  <v-main>
    <v-container class="my-16">
      <v-row>
        <v-col
          
        >
          <h1>Welcome!</h1>
          <v-card
          >
            <v-toolbar color="black" dark flat >
              <v-toolbar-title>Log In Form</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form
                
              >
                <v-text-field
                  v-model="userId"
                  label="User ID"
                >
                </v-text-field>
                
                <v-text-field
                  v-model="userPassword"
                  label="Password"
                >
                </v-text-field>

                <v-btn
                  @click="click()"
                >
                Submit
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</v-app>
</template>

<script>
import myapp from '@/lib/myapp.js'

  export default {
    
    data: () => ({
      duct: null,
      wsdPath: "/ducts/wsd",
      userId: null,
      userPassword: null,
      clientToken: null
    }),

    created: function(){
        this.duct = new myapp.Duct();
        this.duct.logger = new myapp.DuctEventLogger(this.duct);
        this.duct.open(this.wsdPath);


        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("loginFirstPage", {
                success: (data) => {
                  console.log(data);
                  let utf8decoder = new TextDecoder();
                  console.log(utf8decoder.decode(data["RedisKeys"][0]));
                  console.log(utf8decoder.decode(data["RedisKeys2"][0]));
                  //if (data["Auth"]) {
                  this.clientToken = data["ClientToken"];
                  if(this.clientToken === "user not found") {
                    console.log("user not found");
                  }
                  else if (this.clientToken === "password error") {
                    console.log("password error");
                  }
                  else {
                    localStorage.setItem("clientToken", this.clientToken);
                    sessionStorage.setItem("Auth", true);
                    console.log(localStorage.getItem("clientToken"));
                    this.duct.close();
                    window.location.href = `./console`;
                    //this.$router.push({name: "Console", params: { duct: this.duct }});
                    //this.duct.controllers.resourse.createSession(this.userId, this.clientToken)
                  }
                    
                  //}
                  //console.log("data");
                },
                error: (data) => {
                  console.log("error");
                  console.log(data);
                }
            });
            this.duct.eventListeners.resource.on("createSession", {
              success: (data) => {
                console.log(data);
                if(data["Auth"]) {
                  sessionStorage.setItem("Auth", true);
                  this.duct.close();
                  window.location.href = `./console`;
                } else {
                  sessionStorage.removeItem("Auth");
                  localStorage.removeItem("clientToken");
                  localStorage.removeItem("userId");
                }
              }
            });
            let clientToken = localStorage.getItem("clientToken");
            let userId = localStorage.getItem("userId");
            if (clientToken !== null && userId !== null) {
              this.duct.controllers.resource.createSession(userId, clientToken);
            }
        })
    },

    methods: {
      click() {
        //console.log("Click!");
        localStorage.setItem("userId", this.userId);
        this.duct.controllers.resource.loginFirstPage(this.userId, this.userPassword);

      },
      generateRandomString(){
        return Math.random().toString(32).substring(2)
      }
    }
  }
</script>
