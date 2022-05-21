<template>
    <div class="container border-0 align-items-center d-flex justify-content-center">
        <div v-if="links.length > 0" class="jumbotron">
            <h2>
            Please choose {{level}}:
            </h2>
            <div class="btn-group-vertical d-flex justify-content-center">
                <button 
                    class="btn btn-secondary" 
                    @click="selectedLink(link, linkIndex)"
                    v-for="(link, linkIndex) in links"
                    :key="linkIndex" 
                >
                    {{link}}
                </button>
            </div>
        </div>
        <div v-else class="jumbotron">
            <h3>
            No {{level}}s to select, please go back!
            </h3>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        links: {
            type: Array,
            required: true
        },
        level: {
            type: String,
            required: true
        }
    },
    methods: {
        selectedLink(link, linkIndex){
            this.$emit('selectedLink', link, linkIndex);
        }
    }
}
</script>

<style scoped>

</style>