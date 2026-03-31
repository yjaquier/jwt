<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // Import font awesome icon component

const router = useRouter()

const item = ref("Clean the garage")

type todo_item = {
  "id": number,
  "item": string
}

const todos: Ref<todo_item[]> = ref([])

async function get_todos(): Promise<object[] | object> {
  // const data=new FormData()
  // data.append('username', loginForm.value.username)
  // data.append('password', loginForm.value.password)
  return await fetch('http://localhost:8181/todos', {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
  }).then(async response => {
    // console.log(response)
    if (!response.ok) {
      const msg = await response.json()
      // console.log(msg)
      window.alert("Get todos failed !\n" + msg.detail.Error)
      throw new Error(response.statusText);
    }
    else {
      // Handling empty response .json() function on an empty response generate below error
      // Uncaught SyntaxError: Unexpected end of JSON input
      return response.json().catch((error) => {
        console.log('Empty response from API call: ' + error)
        return null
      })
    }
  }).then(data => {
    // console.log(data)
    todos.value = data
    return data
    }).catch(error => {
    console.log("Problem while running /todos (GET) fastAPI endpoint:\n", error)
    return []
  })
}

async function create_todo(): Promise<object[] | object> {
  // const data=new FormData()
  // data.append('username', loginForm.value.username)
  // data.append('password', loginForm.value.password)
  return await fetch('http://localhost:8181/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify({ "item": item.value })
  }).then(async response => {
    // console.log(response)
    if (!response.ok) {
      const msg = await response.json()
      // console.log(msg)
      window.alert("Login failed !\n" + msg.detail.Error)
      throw new Error(response.statusText);
    }
    else {
      // Handling empty response .json() function on an empty response generate below error
      // Uncaught SyntaxError: Unexpected end of JSON input
      return response.json().catch((error) => {
        console.log('Empty response from API call: ' + error)
        return null
      })
    }
  }).then(data => {
    // console.log(data)
    window.alert("Todo " + item.value + " inserted !")
    get_todos() // We can do much better by getting, in retrun, the item id and modify the reactive variable
    return data
    }).catch(error => {
    console.log("Problem while running /todas (POST) fastAPI endpoint:\n", error)
    return []
  })
}

async function delete_todo(id: number): Promise<object[] | object> {
  // const data=new FormData()
  // data.append('username', loginForm.value.username)
  // data.append('password', loginForm.value.password)
  return await fetch('http://localhost:8181/todos/' + id, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify({ 'id': id })
  }).then(async response => {
    // console.log(response)
    if (!response.ok) {
      const msg = await response.json()
      // console.log(msg)
      window.alert("Login failed !\n" + msg.detail.Error)
      throw new Error(response.statusText);
    }
    else {
      // Handling empty response .json() function on an empty response generate below error
      // Uncaught SyntaxError: Unexpected end of JSON input
      return response.json().catch((error) => {
        console.log('Empty response from API call: ' + error)
        return null
      })
    }
  }).then(data => {
    // console.log(data)
    window.alert("Todo " + id + " deleted !")
    get_todos() // We can do much better by getting, in retrun, the item id and modify the reactive variable
    return data
    }).catch(error => {
    console.log("Problem while running /todas/{toto_id} (DELETE) fastAPI endpoint:\n", error)
    return []
  })
}

onMounted(() => {
  get_todos()
})
</script>

<template>
  <main>
    <section>
      <h1>Todo List</h1>
    </section>

    <fieldset class="flex-container">
      <legend>Insert todo in list</legend>

      <div>
        <label for="item">Todo item: </label>
        <input
          id="item"
          v-model="item"
          required
          type="text"
        />
      </div>

      <div>
        <button @click="create_todo">Create</button>
        <button @click="router.push('/')">Home</button>
      </div>
    </fieldset>
    <fieldset class="flex-container">
      <legend>Existing Todo(s)</legend>
      <div v-if="todos.length != 0">
        <table>
          <tr><th>Delete?</th><th>Id</th><th>Item</th></tr>
          <tr v-for="(todo) in todos" :key="todo.id">
            <td>
              <font-awesome-icon style="color: red; cursor: pointer;"
                icon="fa-solid fa-xmark"
                @click="delete_todo(todo.id)"
              />
            </td>
            <td>{{ todo.id }}</td>
            <td>{{ todo.item }}</td>
          </tr>
        </table>
      </div>
    </fieldset>
  </main>
</template>

<style scoped lang="scss">

</style>