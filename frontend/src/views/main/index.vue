
<script setup lang="ts">
import { ref } from 'vue';
import MenuView from '@/views/menu/index.vue';
import EarthView from '@/views/earth/index.vue'
const sDrawer = ref(true);
const habitatID = ref(106);

const setHabitatID = (id) => {
    habitatID.value = id;
    console.log("ID", id);
}

</script>

<template>
    <MenuView :habitatID="habitatID"></MenuView>
    <EarthView :setHabitatID="setHabitatID"></EarthView>
</template>
