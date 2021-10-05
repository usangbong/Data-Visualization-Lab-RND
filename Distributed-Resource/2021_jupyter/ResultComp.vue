<template>
  <div>
    <div class="SectionTitle">
      <h3> Result</h3>
    </div>
    <v-card class="ModelResultContainer" elevation="4">
      <!--
        <ul class="flex-container">
        <li class="flex-item FirstLi">1</li>
        <li class="flex-item SecondLi">2</li>
        <li class="flex-item ThirdLi">3</li>
        <li class="flex-item FourthLi">4</li>
        <li class="flex-item FifthLi">5</li>
        <li class="flex-item SixthLi">6</li>
      </ul>
      -->
      <div class="CardWrapper">
        <div class="CardContainer">
          <v-card class="CardComponent FirstCard" elevation="4">a
          </v-card>
          <v-card class="CardComponent SecondCard" elevation="4">b
          </v-card>
          <v-card class="CardComponent ThirdCard" elevation="4">c
          </v-card>
          <v-card class="CardComponent FourthCard" elevation="4">d
          </v-card>
          <v-card class="CardComponent FifthCard" elevation="4">d
          </v-card>
          <v-card class="CardComponent SixthCard" elevation="4">d
          </v-card>
          <v-card class="CardComponent SeventhCard" elevation="4">d
          </v-card>
          <v-card class="CardComponent EighthCard" elevation="4">d
          </v-card>
        </div>
        <div center>
        <h2 id="MainColor"> Main Color </h2>
        </div>
      </div>
        <br><div> dlResult : {{ dlResult }}</div>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'

Vue.component('child-component', {
  template: '<p>{{ val }}</p>',
  props: ['val'], // 받는 속성 이름을 지정
  mounted() {
    console.log(this.val)
  },
})

export default {
  name: 'ResultComponent',
  data: () => ({
    dlResult: '',
  }),methods: {
    functionSetResult: function(e) {
      console.log("functionSetResult"+e)
      
    },
  }
}

</script>

<style scoped>
#MainColor {
  text-align: center;
}
.ModelResultContainer{
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 1870px;
    height: 250px;
    margin-right: auto;
    margin-left: auto;
    margin-top: 25px;
}
.CardContainer{
    width: 1870px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.SectionTitle{
    width: 1870px;
    height: 20px;
    margin-left: auto;
    margin-top: 50px;
    color: rgb(128, 126, 126);
}

.CardComponent {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
  margin: 10px;
}
.FirstCard {
  background-color: rgba(253,205,172, 0.7) !important;
}
.SecondCard {
  background-color: rgba(203,213,232,0.7) !important;
}
.ThirdCard {
  background-color: rgba(244,202,228, 0.7) !important;
}
.FourthCard {
  background-color: rgba(230,245,201,0.7) !important;
}
.FifthCard {
  background-color: rgba(179,226,205,0.7) !important;
}
.SixthCard {
  background-color: rgba(255,242,174,0.7) !important;
}
.SeventhCard {
  background-color: rgba(241,226,204,0.7) !important;
}
.EighthCard {
  background-color: rgba(204,204,204,0.7) !important;
}
.flex-container {
  /* We first create a flex layout context */
  display: flex;
  flex-flow: row wrap;
  justify-content: space-around;
  padding: 10px;
  margin: 0;
  list-style: none;
}

.flex-item {
  background: tomato;
  padding: 5px;
  width: 200px;
  height: 150px;
  margin-top: 10px;
  line-height: 150px;
  color: white;
  font-weight: bold;
  font-size: 3em;
  text-align: center;
}
</style>