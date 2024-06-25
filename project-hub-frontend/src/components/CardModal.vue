<template>
    <CustomModal :isVisible="isVisible" @close="this.$emit('close')">
      <h2>Créer un ticket</h2>
      {{ newFields }}
      <div class="grid">
        <div class="input-with-label" v-for="field, index in Object.keys(card.fields)" :key="index">
          <span class="field-name">{{ field }}</span>
          <span class="field-type">{{ card.fields[field].type }}</span>
          <CustomSelectMembers multiSelect=true v-if="card.fields[field].type.startsWith('LIST')"
          :options="project.users?.map(e=>e.username)"
          :returnedValues="project.users?.map(e=>e.id)"
          class="select"
          @input="e => getMembersSelected(field, e)"
          />
          <input type="text" v-model="newFields[field]" v-else>
        </div>
      </div>
      <div class="button" @click="editCard(card.cardId, newFields)">
        Sauvegarder les modifications
      </div>
    </CustomModal>
  </template>
  
  <script>
  import CustomModal from "./CustomModal.vue";
  import CustomSelectMembers from "./CustomSelect.vue";
  import { getProject, editCard } from "@/js/api.js";
  export default {
    name: 'CardModal',
    components: {CustomModal, CustomSelectMembers},
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
      getMembersSelected(field, data) {
        this.newFields[field] = data;
      },
      closeModal() {
        this.$emit('close');
      },
      async getProject() {
        return await getProject(this.projectId);
      },
      async editCard(cardId, newFields) {
        await editCard(cardId, newFields);
      }
    },
    data: () => ({
        projectId: 1,
        project: null,
        newFields: {}
    }),
    async mounted() {
        this.project = await this.getProject();
        // this.newFields = this.card.fields;
    },
    watch: {
      isVisible(v) {
        if (v) {
          Object.keys(this.card.fields).map(key=> {
            this.newFields[key] = this.card.fields[key].value
          })
          return
        }
      }
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
  .field-name {
    padding: 1rem;
  }
  .field-type {
    padding: 1rem;
  }

  .input-with-label {
    display: grid;
    grid-template-columns: 33% 33% 34%;
    height: 100%;
  }
  </style>
  