<template>
<v-main>
  <div class="ma-1">
    <!--<p><input type="range" min="0" max="100" v-model.number="radius"></p>-->
    <p><v-btn width="400" @click="testStart()">start</v-btn></p>
    <p><v-btn width="400" @click="runStage=false;">end</v-btn></p>
  </div>
</v-main>
</template>

<script>
export default {
  props: ["duct"],
  data() {
    return {
      radius: 25,
      runStage: false,
    }
  },
  methods: {
      testStart() {
          //let data = {};
          for (let i = 0; i < 4; i++) {
            //data["floatArray"] = [0,0]; data["str"] = "ready"; data["num"] = i; data["user_num"] = 4; data["intArray"] = [0,1,2,3];
            //data2 = {'GAME': True, 'floatArray': datadata["floatArray"], 'str': datadata["str"], 'num': datadata["num"], 'user_num': datadata["user_num"], 'intArray': datadata["intArray"]}
            //console.log(data)
            //console.log(JSON.stringify(data));
            //data = "{'floatArray':[0,0],'str':'ready','num':0,'user_num':4,'intArray':[0,1,2,3]}"
            //data = '{"floatArray":[0,0],"str":"ready","num":0,"user_num":4,"intArray":[0,1,2,3]}'
            this.duct.controllers.resource.ackCoordinate([0,0], "ready", i, 4, [0,1,2,3]);
          }
      }
  }
}
</script>