<script setup lang="ts">

const props = defineProps(['state'])

</script>

<template>
    <label class="switch">
        <input v-bind:class="(props.state)?'isChecked' : ''" type="checkbox">
        <span class="slider round"></span> 
    </label>
</template>

<style scoped>

/* this comes from w3schools */

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

.isChecked + .slider {
  background-color: var(--color-foreground);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--color-foreground);
}

.isChecked + .slider:before {
  -webkit-transform: translateX(20x);
  -ms-transform: translateX(20px);
  transform: translateX(20px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>