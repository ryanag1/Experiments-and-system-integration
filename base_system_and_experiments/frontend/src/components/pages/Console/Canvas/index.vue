<template>
<v-main>
  <div class="ma-1">
    <MyCanvas :runStage="runStage"/>
    <!--<p><input type="range" min="0" max="100" v-model.number="radius"></p>-->
    <p><v-btn width="400" @click="runStage=true;">start</v-btn></p>
    <p><v-btn width="400" @click="runStage=false;">end</v-btn></p>
  </div>
</v-main>
</template>

<script>
// キャンバス用コンポーネントの読み込み
import MyCanvas from './MyCanvas.vue'
export default {
  components: {
    MyCanvas
  },
  data() {
    return {
      radius: 25,
      runStage: false,
    }
  }
}
</script>