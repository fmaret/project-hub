 
<template>
    <div class="custom-select" :tabindex="tabindex" @blur="open = false">
        <div class="selected" :class="{ open: open }" @click="open = !open">
        {{ selected }}
        </div>
        <div class="items" :class="{ selectHide: !open }">
        <div
            v-for="(option, i) of options"
            :key="i"
            @click="selectOption(option, i)"
        >
            {{ option }}
        </div>
        </div>
    </div>
  </template>
  
  <script>
  // default is not compatible with returnedValues
  export default {
    name: 'CustomSelect',
    props: {
        options: {
            type: Array,
            required: true,
        },
        returnedValues: {
            type: Array,
            required: false,
        },
            default: {
            type: String,
            required: false,
            default: null,
        },
            tabindex: {
            type: Number,
            required: false,
            default: 0,
        },
        multiSelect: {
            type: Boolean,
            default: false
          }

    },
    methods: {
      selectOption(option, i) {
        if (!this.multiSelect) {
          this.selected = option;
          this.selectedReturnedValues = this.returnedValues[i];
        } else {
          console.log("AAA", this.selectedReturnedValues, this.selectedReturnedValues.includes(this.returnedValues[i]))
          this.selected.includes(option) ? this.selected.pop(option) : this.selected.push(option);
          if (this.selectedReturnedValues.length > 0) this.selectedReturnedValues.includes(this.returnedValues[i]) ? this.selectedReturnedValues.pop(this.returnedValues[i]) : this.selectedReturnedValues.push(this.returnedValues[i]);
          else this.selectedReturnedValues.push(this.returnedValues[i]);
        }
        this.open = false;
        this.$emit('input', this.returnedValues.length > 0 ? this.selectedReturnedValues : this.selected);
      }
    },
    data: () => ({
        selected: null,
        open: false,
        selectedReturnedValues: []
    }),
    mounted() {
        this.selected = this.default ? this.default : this.options.length > 0 && !this.multiSelect ? this.options[0] : this.multiSelect ? [] : null;
        this.$emit("input", this.selected);
    },  
    watch: {
      options() {
        this.selected = this.default ? this.default : this.options.length > 0 && !this.multiSelect ? this.options[0] : this.multiSelect ? [] : null;
        if (this.returnedValues.length > 0) this.selectedReturnedValues = this.returnedValues[0];
        this.$emit("input", this.returnedValues ? this.selectedReturnedValues : this.selected);
      }
    },
  }
  </script>
  
  <style scoped>
  .custom-select {
    position: relative;
    width: 100%;
    text-align: left;
    outline: none;
    height: 47px;
    line-height: 47px;
  }
  
  .custom-select .selected {
    background-color: #0a0a0a;
    border-radius: 6px;
    border: 1px solid #666666;
    color: #fff;
    padding-left: 1em;
    cursor: pointer;
    user-select: none;
  }
  
  .custom-select .selected.open {
    border: 1px solid #ad8225;
    border-radius: 6px 6px 0px 0px;
  }
  
  .custom-select .selected:after {
    position: absolute;
    content: "";
    top: 22px;
    right: 1em;
    width: 0;
    height: 0;
    border: 5px solid transparent;
    border-color: #fff transparent transparent transparent;
  }
  
  .custom-select .items {
    color: #fff;
    border-radius: 0px 0px 6px 6px;
    overflow: hidden;
    border-right: 1px solid #ad8225;
    border-left: 1px solid #ad8225;
    border-bottom: 1px solid #ad8225;
    position: absolute;
    background-color: #0a0a0a;
    left: 0;
    right: 0;
    z-index: 1;
  }
  
  .custom-select .items div {
    color: #fff;
    padding-left: 1em;
    cursor: pointer;
    user-select: none;
  }
  
  .custom-select .items div:hover {
    background-color: #ad8225;
  }
  
  .selectHide {
    display: none;
  }
  </style>
  