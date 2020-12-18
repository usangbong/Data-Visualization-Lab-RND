<template>
  <v-app>
    <v-app-bar
      app
      color="rgba(245, 245, 245,1)"
      dark
      class="appbar"
    >
      <div class="d-flex align-center">
        <v-img
          alt="VislabLogo"
          class="VislabLogo"
          contain
          src="./assets/logo.png"
          transition="scale-transition"
          width="40"
        />
        <h1 class="Title">Photovoltaic Forecasting VA</h1>
      </div>

      <v-spacer></v-spacer>

      <div>
        <v-btn
          class="appbar-btn"
          text
          icon
          color="grey"
        >
          <v-icon large aria-hidden="false">
            mdi-cog-box
          </v-icon>
        </v-btn>
      </div>
    </v-app-bar>

    <v-main>
      <ModelDesignComp/>
      <ResultComp/>
      <TestComp/>
      <ChildComp/>
    </v-main>
  </v-app>
</template>

<script>
import TestComp from './components/TestComp.vue';
import ModelDesignComp from './components/ModelDesignComp';
import ResultComp from './components/ResultComp';
import ChildComp from './components/ChildComp';

export default {
  name: 'App',

  components: {
    ModelDesignComp,ResultComp,TestComp, ChildComp
  },
  computed: {

  },

};
</script>

<style scoped>
#app{
  width:1920px;
  height:1080px;
  /*border:1px solid;*/
  box-sizing: border-box;
  margin-right: auto;
  background:rgba(245, 245, 245,1);
  font-family: 'Material Design Icons';
}
.appbar{
  width:1920px;
  min-width:1920px;
  margin-right: auto;
  padding-left: 10px;
  padding-right: 10px;
  color: rgba(0, 0, 0, 0.87);
  box-shadow: 0 0 black !important;
}
.Title{
  padding-left: 10px;
}
</style>