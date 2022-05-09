<template>
    <div class="container border-0 align-items-center d-flex justify-content-center">
        <div class="jumbotron">
            <h2>
            Please choose a {{level}}:
            </h2>
            <div class="btn-group-vertical d-flex justify-content-center">
                <button 
                    class="btn btn-secondary" 
                    @click="selectedLink(link)"
                    v-for="(link, linkIndex) in links"
                    :key="linkIndex" 
                >
                    {{link}}
                </button>
            </div>
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
        selectedLink(link){
            this.$emit('selectedLink', link);
        }
    }
}
</script>

<style scoped>
.breadcrumb {
    background-color: white;
    border: 1px solid rgba(0,0,0,0.125);
    border-radius: 0.37rem;
}

</style>