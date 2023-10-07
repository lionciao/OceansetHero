<script setup lang="ts">
/*Call Components*/
import mapboxgl from 'mapbox-gl';
import * as turf from '@turf/turf';
import { onMounted, toRefs, ref, watch } from 'vue';

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_KEY

const map = ref(null);
const mapLayersId = ref([])
const props = defineProps<{
    setHabitatID: Function
    habitats: Object
    clickItemId: Number
}>()
var center = [-77.574732, 44.007793]
var marker = {}


watch(() => props.habitats, (habitats) => {
    console.log("habitats changed", habitats)
    console.log("map", map.value)

    if (map.value) {
        clearMap();
        drawPolygon();
    }
});


const clearMap = () => {
    if (mapLayersId.value.length) {
        mapLayersId.value.forEach((id) => {
            map.value.removeLayer(id);
            map.value.removeSource(id);
        })
        mapLayersId.value = []
        marker.remove()
    }
};

const calCenterCor = (cor) => {
    var polygon = turf.polygon(cor)
    const center = turf.centerOfMass(polygon).geometry.coordinates;
    return center
}

const drawPolygon = () => {
    props.habitats.forEach((habitat) => {
        const polygonData = {
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    properties: {},
                    geometry: {
                        type: 'Polygon',
                        coordinates: habitat.polygon,
                    },
                },
            ],
        };
        // console.log("habitat.polygon")

    polygonData.features.forEach(feature => {
        const center = turf.centerOfMass(feature).geometry.coordinates
        polygon_center.push(center)
    });

    const map = new mapboxgl.Map({
        container: 'map-container',
        style: 'mapbox://styles/chiyuwu/clnfm6w8501km01r76g4bgg57',
        center: [-81.91673000044847, 43.227219998996674],
        zoom: 15,
    });

    // draw water region
    map.on('load', () => {
        map.addSource('polygon', {
            type: 'geojson',
            data: polygonData,
        });

        map.value.addLayer({
            id: `polygon-${habitat.id}`,
            type: 'fill',
            source: `polygon-${habitat.id}`,
            layout: {},
            paint: {
                'fill-color': '#8d05f5',
                'fill-opacity': 0.5
            },
        });
        console.log(`polygon-${habitat.id}`)

        // add region center tag
        polygon_center.forEach((center, index) => {
            const marker = new mapboxgl.Marker({ className: "water-detail-marker" })
                .setLngLat(center)
                .addTo(map);

            // popup the details of water region
            marker.getElement().addEventListener('click', () => {
                new mapboxgl.Popup({ className: "water-detail-popup" })
                    .setLngLat(center)
                    .setHTML(`<h1>Detail of Center ${index + 1}</h1>`)
                    .addTo(map);
            });
        });

        map.on('click', 'polygon', (e) => {
            const features = map.queryRenderedFeatures(e.point, { layers: ['polygon'] });
            props.setHabitatID(166);

            if (features.length > 0) {
                console.log('Clicked on polygon:', habitat);
                props.setHabitatID(habitat.id)
                marker.remove()
                center = calCenterCor(polygonData.features[0].geometry.coordinates);
                marker = new mapboxgl.Marker({ className: 'habitat-marker' })
                    .setLngLat(center)
                    .addTo(map.value);
            }
        });

        if (habitat.id == props.clickItemId) {
            center = calCenterCor(polygonData.features[0].geometry.coordinates);
            console.log("center", center)
            marker = new mapboxgl.Marker({ className: 'habitat-marker' })
                .setLngLat(center)
                .addTo(map.value);
        }

        mapLayersId.value.push(`polygon-${habitat.id}`);
    })

    map.value.setCenter(center);
    map.value.setZoom(12);
}


onMounted(() => {
    map.value = new mapboxgl.Map({
        container: 'map-container',
        style: 'mapbox://styles/chiyuwu/clnfm6w8501km01r76g4bgg57',
        center: [-77.574732, 44.007793],
        zoom: 12,
    });


});
</script>

<template>
    <div style="width: 100%; height: 100vh; padding: 0%;">
        <div style="width: 100%; height: 100vh; padding: 0%;" id="map-container"></div>
    </div>
</template>

<style>
.water-region-popup .mapboxgl-popup-close-button {
    display: none;
}

.water-region-popup .mapboxgl-popup-content {
    background-color: rgba(76, 130, 239, 0.848);
    font: 100 8px/15px Sans-serif;
    color: rgb(255, 255, 255);
    padding: 10px;
}

.water-region-popup .mapboxgl-popup-tip {
    border-top-color: rgba(76, 130, 239, 0.848);
}

.water-detail-popup .mapboxgl-popup-close-button {
    display: none;
}

.water-detail-popup .mapboxgl-popup-content {
    background-color: rgba(76, 130, 239, 0.848);
    font: 100 8px/15px Sans-serif;
    color: rgb(255, 255, 255);
    padding: 10;
}

.water-detail-popup .mapboxgl-popup-tip {
    border-top-color: rgba(76, 130, 239, 0.848);
}
</style>