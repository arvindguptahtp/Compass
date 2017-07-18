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


<comments>
class="tx--small--f3--900--tcU--aa rxn--shade20 fx--shift",
o-base="row--pGrid--sMiddle mod--balance pad--x25 pad--y25 rhy--xStart25"
</comments>
