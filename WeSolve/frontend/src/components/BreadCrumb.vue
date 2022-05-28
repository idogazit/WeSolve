<template>
    <div class="border-0">
        <nav>
            <ol class="breadcrumb">
                <li
                    v-for="(crumb, ci) in crumbs"
                    :key="ci"
                    class="breadcrumb-item align-items-center"
                >
                    <button class="btn btn-link" :class="{ disabled: isLast(ci) }" @click="selected(crumb, ci)">
                        {{crumb}}
                    </button>
                </li>
            </ol>
        </nav>
    </div>
</template>

<script>
export default {
    props: {
        crumbs: {
            type: Array,
            required: true
        },
        inQuestion: {
            type: Boolean,
            required: true
        }
    },
    methods: {
        isLast(index){
            return index === this.crumbs.length - 1 && !this.inQuestion;
        },
        selected(crumb, ci){
            this.$emit('selected', crumb, ci);
            localStorage.removeItem('newSlug');
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