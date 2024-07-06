<template>
    <CustomModal :isVisible="isVisible" :title="createTicket ? 'Créer un ticket' : 'Editer un ticket'" @close="this.$emit('close')">
      {{ newFields }}
      <div class="card-modal-content">
        <div class="card-modal-content-top">aze</div>
        <EditableText :text="card.fields['title'].value" class="title"
        @edited-text="newVal => updateField('title', newVal)"
        />
        <div class="card-modal-content-body">
          <div class="card-modal-content-left">
            <template v-for="field, index in ['description', 'assignees']" :key="index">
              <CardFieldEdition :fieldName="field" :fieldObject="card.fields[field]" :fieldDefaultValue="newFields[field]" :project="project"
              @field-updated="newVal => updateField(field, newVal)"
              />
            </template>
          </div>
          <div class="card-modal-content-right">aze</div>
        </div>
       
      </div>
      <div class="grid" v-if="!createTicket & false">
        <div class="input-with-label" v-for="field, index in Object.keys(card.fields)" :key="index">
          <span class="field-name">{{ field }}</span>
          <span class="field-type">{{ card.fields[field].type }}</span>
          <CustomSelect :multiSelect="card.fields[field].type.startsWith('LIST')" v-if="/MEMBER/.test(card.fields[field].type)"
          :options="project.users?.map(e=>e.username)"
          :returnedValues="project.users?.map(e=>e.id)"
          :default="project.users?.filter(e=>card.fields[field].value ? card.fields[field].value.includes(e.id) : false).map(e=>e.username)"
          class="select"
          @input="e => getMembersSelected(field, e)"
          />
          <CustomSelect :multiSelect="card.fields[field].type.startsWith('LIST')" v-else-if="/ENUM/.test(card.fields[field].type)"
          :options="getCardEnumOptions(card, field)"
          :default="card.fields[field].value"
          class="select"
          @input="e => newFields[field] = e"
          />
          <input type="text" v-model="newFields[field]" v-else>
        </div>
      </div>
      <div v-else-if="Object.keys(cardTypes).length > 0">
        <div class="input-with-label">
          <span class="field-name">Type de carte</span>
          <CustomSelect
          :options="cardTypes.map(e=>e.cardType)"
          :returnedValues="cardTypes.map(e=>e.cardTypeId)"
          class="select"
          @input="changeSelectedCardType"
          />
        </div>
        <div class="grid">
          <div class="input-with-label" v-for="field, index in Object.keys(this.cardTypeFields)" :key="index">
            <span class="field-name">{{ field }}</span>
            <span class="field-type">{{ this.cardTypeFields[field].type }}</span>
            <CustomSelect :multiSelect="cardTypeFields[field].type.startsWith('LIST')" v-if="/MEMBER/.test(cardTypeFields[field].type)"
            :options="project.users?.map(e=>e.username)"
            :returnedValues="project.users?.map(e=>e.id)"
            :default="project.users?.filter(e=>cardTypeFields[field].value ? cardTypeFields[field].value.includes(e.id) : false).map(e=>e.username)"
            class="select"
            @input="e => getMembersSelected(field, e)"
            />
            <CustomSelect :multiSelect="cardTypeFields[field].type.startsWith('LIST')" v-else-if="/ENUM/.test(cardType.fields[field].type)"
            :options="getCardEnumOptions(cardType, field)"
            :default="cardTypeFields[field].value"
            class="select"
            @input="e => newFields[field] = e"
            />
            <input type="text" v-model="newFields[field]" v-else>
          </div>
        </div>
      </div>

      <div v-if="createTicket" class="button" @click="createCard(newFields)">
        Créer le ticket
      </div>
      <div v-else class="button" @click="editCard(card.cardId, newFields)">
        Sauvegarder les modifications
      </div>
    </CustomModal>
  </template>
  
  <script>
  import CustomModal from "./CustomModal.vue";
  import CustomSelect from "./CustomSelect.vue";
  import EditableText from "./EditableText.vue";
  import CardFieldEdition from "./CardFieldEdition.vue";

  import { getProject, editCard, getCardTypes, createCard } from "@/js/api.js";
  export default {
    name: 'CardModal',
    components: {CustomModal, CustomSelect, EditableText, CardFieldEdition},
    props: {
      isVisible: {
        type: Boolean,
        required: true
      },
      card: {
        required: true
      },
      createTicket: {
        type: Boolean,
        required: false,
        default: false
      }
    },
    methods: {
      updateField(field, newVal){
        this.newFields[field] = newVal;
      },
      getCardEnumOptions(card, field) {
        return card.fields[field].values[card.fields[field].type.split("_")[1].split("]")[0]];
      },
      changeSelectedCardType(e) {
        this.selectedCardTypeId = e; 
      },
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
        this.$emit("card-updated");
      },
      async createCard(newFields) {
        await createCard(this.projectId, this.selectedCardTypeId, newFields);
        this.$emit("card-updated");
      }
    },
    data: () => ({
        projectId: 1,
        project: null,
        newFields: {},
        cardTypes: [],
        selectedCardTypeId: null,
    }),
    async mounted() {
        this.project = await this.getProject();
        // this.newFields = this.card.fields;
    },
    watch: {
      async isVisible(v) {
        this.newFields = {};
        if (v && this.createTicket) this.cardTypes = (await getCardTypes(this.projectId)).cardTypes;
        if (v && !this.createTicket) {
          Object.keys(this.card.fields).map(key=> {
            this.newFields[key] = this.card.fields[key].value;
          })
          return
        }
      }
    },
    computed: {
      cardType() {
        if (Object.keys(this.cardTypes).length > 0 && this.selectedCardTypeId) console.log("aze", this.cardTypes, this.selectedCardTypeId);
        return Object.keys(this.cardTypes).length > 0 && this.selectedCardTypeId ? this.cardTypes.filter(e=>e.cardTypeId == this.selectedCardTypeId)[0] : {};
      },
      cardTypeFields() {
        console.log("coucou", this.cardType, this.cardType.fields);
        return this.cardType.fields ? this.cardType.fields : {};
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
    padding: 4rem;
    border-radius: 0.5rem;
    width:80%;
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

  .title {
    font-size: 25px;
  }

  .card-modal-content {
    padding-left: 1rem;
  }

  .card-modal-content-top {
    background-color: lightcoral;
  }

  .card-modal-content-right {
    background-color: lightgreen;
  }

  .card-modal-content-left {
    background-color: lightblue;
    display: flex;
    flex-direction: column;
  }

  .card-modal-content-body {
    display: grid;
    grid-template-columns: 70% 30%;
    height: 100%;
  }
  </style>
  