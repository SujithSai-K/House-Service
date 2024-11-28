<template>
  <div>
    <form @submit.prevent="post">
      <input type="text" v-model="name" placeholder="Name">
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: ''
    }
  },
  methods: {
    async post() {
      console.log("Post function called");
      console.log(this.name);
      // You can even test with a simple axios call
      // await axios.post('your_endpoint', { name: this.name });
    }
  }
}
</script>
