<script>
    export default {
        name: 'fold-unfold',
        props: {
            init: Boolean,
            title: String,
            styles: Object
        },
        data () {
            return {
                fold: this.init || false
            }
        },
        methods: {
            update (ev) {
                this.fold = !this.fold
                ev.target.blur()
            }
        },
        computed: {
            menu_icon () {
                if (this.fold) {
                    return "#ico--menu"
                }
                else {
                    return "#ico--menu-close"
                }
            }
        }
    }
</script>


<template lang="pug" src="./fold-unfold.js.pug"></template>
