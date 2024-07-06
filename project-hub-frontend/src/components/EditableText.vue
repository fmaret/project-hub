<template>
  <div class="editable-text">
    <span v-if="!editText" @click="editText = true">{{editedText}}</span>
    <input v-else v-on:keyup.enter="validateText" v-model="editedText"/>
  </div>
</template>
  
<script>
  export default {
    name: 'EditableText',
    props: {
      text: {
        type: String,
        required: true
      }
    },
    methods: {
      validateText(e) {
        this.editedText = e.target.value;
        this.editText = false;
        this.$emit("edited-text", this.editedText);
      }
    },
    data: () => ({
      editText: false,
      editedText: null,
    }),
    mounted() {
      this.editedText = this.text;
    },  
    watch: {
    }
  }
</script>

<style scoped>

input {
  text-align: center;
  font-size:16px;
}

input:focus {
  outline: none;

}

.editable-text {
  display: flex;
}

</style>
