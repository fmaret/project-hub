<template>
    <CustomModal :isVisible="isVisible" @close="this.$emit('close')">
      <h2>Créer un ticket</h2>
      <div class="input-with-label" v-for="field, index in Object.keys(card.fields)" :key="index">
        <span>{{ field }}</span>
        <span>{{ card.fields[field].type }}</span>
        <CustomSelect v-if="card.fields[field].type.startsWith('LIST')"
        :options="project.users?.map(e=>e.username)"
        :default="'Florent'"
        class="select"
        />
        <input type="text" v-else>
      </div>
      <div class="button" @click="editCard(card.cardId)">
        Sauvegarder les modifications
      </div>
    </CustomModal>
  </template>
  
  <script>
  import CustomModal from "./CustomModal.vue";
  import CustomSelect from "./CustomSelect.vue";
  import { getProject, editCard } from "@/js/api.js";
  export default {
    name: 'CardModal',
    components: {CustomModal, CustomSelect},
    props: {
      isVisible: {
        type: Boolean,
        required: true
      },
      card: {
        required: true
      }
    },
    methods: {
      closeModal() {
        this.$emit('close');
      },
      async getProject() {
        return await getProject(this.projectId);
      },
      async editCard(cardId) {
        await editCard(cardId);
      }
    },
    data: () => ({
        projectId: 1,
        project: null,
    }),
    async mounted() {
        this.project = await this.getProject();
    }
  }
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    position: relative;
  }
  
  .close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
  }

  .button {
    background-color: darkgreen;
    color: white;
    padding: 1rem;
    margin: 1rem;
  }

  .button:hover {
    cursor: pointer;
  }
  </style>
  