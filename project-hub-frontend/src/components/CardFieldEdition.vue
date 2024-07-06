<template>
  <div class="editable-input">
    <span class="editable-input-title">{{ fieldName }}</span>
    <template v-if="!editInput">
      <span class="editable-input-value" @click="editInput = true;">
        {{ displayValue(fieldDefaultValue) }}
      </span>
    </template>
    <template v-else>
      <CustomSelect :multiSelect="fieldObject.type.startsWith('LIST')" v-if="/MEMBER/.test(fieldObject.type)"
      :options="project.users?.map(e=>e.username)"
      :returnedValues="project.users?.map(e=>e.id)"
      :default="project.users?.filter(e=>fieldObject.value ? fieldObject.value.includes(e.id) : false).map(e=>e.username)"
      class="select"
      @input="e => getMembersSelected(field, e)"
      @blur="blurEditableInput()"
      />
      <CustomSelect :multiSelect="fieldObject.type.startsWith('LIST')" v-else-if="/ENUM/.test(fieldObject.type)"
      :options="getCardEnumOptions(card, field)"
      :default="fieldObject.value"
      class="select"
      @input="e => e"
      @blur="blurEditableInput()"
      />
      <input type="text" v-model="fieldValue" @blur="blurEditableInput()" v-else>
    </template>
  </div>
</template>
  
<script>
  import CustomSelect from './CustomSelect.vue';

  export default {
    name: 'CardFieldEdition',
    components: {CustomSelect},
    props: {
      fieldName: {
        type: String,
        required: true
      },
      fieldObject: {
        type: Object,
        required: true
      },
      project: {
        type: Object,
        required: true
      },
      fieldDefaultValue: {
        required: true,
      }
    },
    methods: {
      blurEditableInput() {
        this.editInput = false;
        this.$emit("field-updated", this.fieldValue);
      },
      displayValue(val) {
        if (/MEMBER/.test(this.fieldObject.type)) return this.project.users.filter(e=>e.id in this.fieldDefaultValue).map(e=>e.username);
        return val ? val : "[VIDE]";
      },
      getMembersSelected(field, data) {
        this.fieldValue = data;
      },
      getCardEnumOptions(card, field) {
        return card.fields[field].values[card.fields[field].type.split("_")[1].split("]")[0]];
      },
      validateText(e) {
        this.editedInput = e.target.value;
        this.editInput = false;
        this.$emit("input", this.editedInput);
      }
    },
    data: () => ({
      editInput: false,
      editedInput: null,
      fieldValue: null,
    }),
    mounted() {
      this.editedInput = this.text;
      this.fieldValue = this.fieldObject.value;
    },  
    watch: {
    }
  }
</script>

<style scoped>
.editable-input {
  display: flex;
  flex-direction: column;
}

.editable-input-title {
  display: flex;
  align-content: start;
}

.editable-input-value {

}
</style>
