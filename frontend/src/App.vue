<script>
import HeaderComponent from "@/components/HeaderComponent.vue";

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      noHeaderViews: ["Login", "Register"]
    }
  },
  computed: {
    pageName() {
      if (this.$route.name === "Task") {
        return this.taskName;
      }
      return this.$route.name;
    }
  },
};
</script>

<template>
  <HeaderComponent v-if="pageName!==undefined&&!noHeaderViews.includes(pageName)"/>
  <router-view class="router-view"></router-view>
</template>

<style scoped>
.router-view {
  height: 100%;
}

/deep/ .fc a {
  text-decoration: none !important;
  color: inherit;
}
/deep/ .fc-day-today{
  background-color: #e6f7ff !important;
}
</style>
