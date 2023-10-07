
<script setup lang="ts">
import { ref } from 'vue';
import Menu from '@/components/menu/Menu.vue';
const sDrawer = ref(true);

const props = defineProps<{
    habitatID: number
}>()
</script>

<template>
    <v-navigation-drawer width="390" left elevation="0" app class="leftSidebar" v-model="sDrawer">
        <Menu :habitatID="props.habitatID"></Menu>
    </v-navigation-drawer>
</template>
