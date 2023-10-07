<script setup lang="ts">
import mapbox from '@/views/earth/mapbox.vue';
import searchbar from '@/views/earth/searchbar.vue';
import { onMounted, toRefs, ref } from 'vue';
import axios from 'axios';

const habitats = ref([])
const props = defineProps<{
    setHabitatID: Function,
}>()
const clickItemId = ref()

const list = async (lon, lat, id) => {
    const apiUrl = `https://www.oceanset.earth/api/list?latitude=${lat}&longitude=${lon}`;
    axios.get(apiUrl)
        .then((response) => {
            console.log("list",response.data);
            habitats.value = response.data;
            clickItemId.value = id
        })
        .catch((error) => {
            console.error(error);
        });
}

const handleListItemClick = async (result) => {
    console.log('item be clicked')
    await list(result.centre[0], result.centre[1], result.id)
}

onMounted(async () => {
    list(-77.574732, 44.007793, 106)
})


</script>

<template>
    <div class="container" style="padding: 0px;">
        <div class="searchbar">
            <searchbar :handleListItemClick="handleListItemClick" />
        </div>
        <div class="mapbox">
            <mapbox :setHabitatID="props.setHabitatID" :habitats="habitats" :clickItemId="clickItemId" />
        </div>
    </div>
</template>

<style>
.searchbar {
    z-index: 20;
    width: 974px;
    margin: 20px auto;
    /* background-color: #000000; */
    position: absolute;
    top: 5%;
    left: 50%;
    transform: translate(-30%, -50%);
}

.mapbox {
    width: 100vw;
    height: 100vh;
    z-index: 10;
    /* background-color: #4C82EF; */
    /* margin: auto; */
    position: relative;
}

.container {
    width: 100%;
    height: 100vh;
    /* padding: 0px; */
    /* margin: 0px; */
    margin: auto;
}
</style>

