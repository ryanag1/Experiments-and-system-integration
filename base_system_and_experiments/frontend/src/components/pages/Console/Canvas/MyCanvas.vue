<template>
  <canvas width="400" height="600" class="canvas"></canvas>
</template>

<script>
export default {
  props: {
    runStage: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      stage: {
        run: false,
        start: 0,
        end: 0,
        interval: null,
        WIDTH: 400,
        HEIGHT: 600,
      },
      position: {
        x: 200,
        y: 300,
      },
      speed: {
        x: 3,
        y: 5,
      },
      redius: 15,
      /*player: {
        offset: 80,
        width: 80,
        height: 40,
      },*/
      player1: {
        offset: 50,
        width: 80,
        height: 20,
        posx: null,
        posy: null,
        speed: 0,
        upperLx: null,
        upperLy: null,
      },
      player2: {
        offset: 50,
        width: 80,
        height: 20,
        posx: null,
        posy: null,
        speed: 0,
        upperLx: null,
        upperLy: null,
      },
      cond1: -1,
      cond2: -1
    }
  },
  watch: {
    runStage(isRun) {
      this.stage.run = isRun;
      if (isRun) {
        this.start();
      } else {
        this.end();
      }
   },
  },
  methods: {
    init() {
      this.player1.posx = this.stage.WIDTH * 0.5;
      this.player1.posy = this.stage.HEIGHT - this.player1.offset;
      this.player1.upperLx = this.player1.posx - this.player1.width * 0.5;
      this.player1.upperLy = this.player1.posy - this.player1.height * 0.5;

      this.player2.posx = this.stage.WIDTH * 0.5;
      this.player2.posy = this.player2.offset;
      this.player2.upperLx = this.player2.posx - this.player2.width * 0.5;
      this.player2.upperLy = this.player2.posy - this.player2.height * 0.5;

    },
    draw(radius) {
      this.ctx.beginPath()
      this.ctx.clearRect(0, 0, this.stage.WIDTH, this.stage.HEIGHT);
      this.ctx.arc(this.position.x, this.position.y, radius, 0, Math.PI * 2)
      this.ctx.fillStyle = 'black';
      this.ctx.fill()

      this.ctx.beginPath()
      this.ctx.rect(this.player1.upperLx, this.player1.upperLy, this.player1.width, this.player1.height);
      this.ctx.fillStyle = 'black';
      this.ctx.fill()

      this.ctx.beginPath()
      this.ctx.rect(this.player2.upperLx, this.player2.upperLy, this.player2.width, this.player2.height);
      this.ctx.fillStyle = 'black';
      this.ctx.fill()
    },
    moveBySecond() {
      if(this.position.x <= 0 || this.position.x >= this.stage.WIDTH) {
        this.speed.x *= -1;
      }
      if(this.position.y <= 0 || this.position.y >= this.stage.HEIGHT) {
        this.speed.y *= -1;
      }
      this.collision1y()
      this.collision2y()
      this.collision1x()
      this.collision2x()
      if((this.cond1 / this.cond2) >= 2 && (this.cond1 * this.cond2 === 2)) {
        this.speed.y *= -1;
      } else if ( (this.cond1 / this.cond2) <= 0.5 && (this.cond1 * this.cond2 === 2)){
        this.speed.x *= -1;
        //this.speed.y *= -1;
      } 
      this.position.x += this.speed.x;
      this.position.y += this.speed.y;
    },
    collision1y(){
      let y = ( ( this.position.y + this.redius ) >= this.player1.upperLy );
      if(y) {
        if(this.cond1 === -1) { this.cond1 = 1; }
        else if( this.cond1 === 1 ) { this.cond1 = 1; }
        else { this.cond2 = 1; }
      } 
      else if(this.position.y >= this.stage.HEIGHT * 0.5 ){
        if(this.cond1 === 1) { this.cond1 = -1; }
        if(this.cond2 === 1) { this.cond2 = -1; }
      }
    },
    collision1x() {
      let x = (this.position.x >= this.player1.upperLx && this.position.x <= ( this.player1.upperLx + this.player1.width) );
      if(x) {
        if(this.cond1 === -1) { this.cond1 = 2; }
        else if( this.cond1 === 2 ) { this.cond1 = 2; }
        else { this.cond2 = 2; }
      } 
      else if(this.position.y >= this.stage.HEIGHT * 0.5 ){
        if(this.cond1 === 2) { this.cond1 = -1; }
        if(this.cond2 === 2) { this.cond2 = -1; }
      }
    },
    collision2y(){
      let y = ( ( this.position.y - this.redius ) <= (this.player2.upperLy + this.player2.height) );
      if(y) {
        if(this.cond1 === -1) { this.cond1 = 1; }
        else if( this.cond1 === 1 ) { this.cond1 = 1; }
        else { this.cond2 = 1; }
      } 
      else if(this.position.y <= this.stage.HEIGHT * 0.5 ){
        if(this.cond1 === 1) { this.cond1 = -1; }
        if(this.cond2 === 1) { this.cond2 = -1; }
      }
    },
    collision2x() {
      let x = (this.position.x >= this.player2.upperLx && this.position.x <= ( this.player2.upperLx + this.player2.width) );
      if(x) {
        if(this.cond1 === -1) { this.cond1 = 2; }
        else if( this.cond1 === 2 ) { this.cond1 = 2; }
        else { this.cond2 = 2; }
      } 
      else if(this.position.y <= this.stage.HEIGHT * 0.5 ){
        if(this.cond1 === 2) { this.cond1 = -1; }
        if(this.cond2 === 2) { this.cond2 = -1; }
      }
    },


    animationFrame() {
      this.moveBySecond();
      this.draw(this.redius);
      this.stage.interval = requestAnimationFrame(this.animationFrame);
    },
    start() {
      console.log("start")
      this.stage.interval = requestAnimationFrame(this.animationFrame);
    },
    end() {
      console.log("end");
      console.log(this.cond1);
      console.log(this.cond2);
      cancelAnimationFrame(this.stage.interval);
    }
  },
  mounted() {
    // mounted 以降で canvas の DOM にアクセスできる
    // CreateJS などを使うときにも、ここで canvas と紐付ける
    // console.log(this.$el)
    this.ctx = this.$el.getContext('2d')
    this.$el.width = this.stage.WIDTH;
    this.$el.height = this.stage.HEIGHT;
    this.init();
    this.draw(this.radius)
  }
}
</script>

<style scoped>
.canvas {
  border: 1px solid #000;
}
</style>