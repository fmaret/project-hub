<template>
  <div class="dashboard">
    <div class="button" @click="showCreateTicketModal = true">Créer ticket</div>
    <CustomModal :isVisible="showCreateTicketModal" @close="showCreateTicketModal = false">
      <h2>Créer un ticket</h2>
      <div class="input-with-label">
        <span>Nom</span>
        <input type="text">
      </div>
      <div class="input-with-label">
        <span>Description</span>
        <input type="text">
      </div>
      <div class="input-with-label">
        <span>Personnes assignées</span>
        <input type="text">
      </div>
    </CustomModal>

  </div>
</template>

<script>
import CustomModal from "./CustomModal.vue";
export default {
  name: 'DashboardScreen',
  props: {
  },
  components: {
    CustomModal
  },
  methods: {
  },
  data: () => ({
    showCreateTicketModal: false,
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main-screen {
  background-color: grey;
}
.button {
  padding: 1rem;
  margin: 1rem;
  background-color: grey;
}

.button:hover {
  cursor: pointer;
}

.input-with-label > * {
  margin: 0.2rem;
}
</style>
