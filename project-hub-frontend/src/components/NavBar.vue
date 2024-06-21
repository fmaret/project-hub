<template>
  <div class="nav-bar">
    <select>
      <option v-for="project, index in user.projects" :key="index">{{ project.name }}</option>
    </select>
    <div class="nav-bar-button" v-for="page, index in pages" :key="index"
    @click="changePage(page.toLowerCase())"
    >
      {{ page }}
    </div>
  </div>
</template>

<script>
import { getUser } from '@/js/api.js';
export default {
  name: 'NavBar',
  data: () => ({
    user: [],
    pages: ["Dashboard", "Roadmap"]
  }),
  props: {
  },
  methods: {
    changePage(page) {
      this.$router.push(`/${page}`)
    }
  },
  async mounted() {
    this.user = await getUser(1);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.nav-bar {
  background-color: darkgreen;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}
.nav-bar-button {
  background-color: grey;
  padding: 1rem;
  margin: 1rem;
}
</style>
