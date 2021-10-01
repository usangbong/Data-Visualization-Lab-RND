<template>
  <div id="childComp">
    <div class="container">
      <p>Child Component</p>
    </div>
  </div>  
</template>

<script>
/*
import Vue from 'vue'

Vue.component('button-counter', {
  template: '<button v-on:click="incrementCounter">{{ counter }}</button>',
  data: function () {
    return {
      counter: 0
    }
  },
  methods: {
    incrementCounter: function () {
      this.counter += 1
      this.$emit('increment')
    }
  },
})*/
</script>

<!--<style lang="scss">-->
<style scoped>
.childComp {
  border: 1px solid;
  box-sizing: border-box;
  background:rgb(228, 110, 110) !important;
}
</style>