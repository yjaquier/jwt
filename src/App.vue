<script setup lang="ts">
/* add fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import all the icons in Free Solid, Free Regular, and Brands styles */
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

library.add(fas, far, fab)
</script>

<template>
  <RouterView />
</template>

<style lang="scss">
body {
  font-family: Arial, Helvetica, sans-serif;
}

h1 {
  text-align: center;
}

button {
  background-color: #2875e7;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  width: 10rem;
  padding: 15px 32px;
  margin: 4px 2px;
  cursor: pointer;
}

.flex-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.flex-container label {
  width: 30rem;
  margin: 10px;
  padding: 10px;
  text-align: center;  
  font-size: 20px;
}

table, tr, th, td {
  border: solid 1px black;
  text-align: center;
}

table {
  width: 50%;
}

</style>