import FoldUnfold from './forms/fold-unfold.vue'
import { checkstate } from './forms/lib.js'
import Slideover from './modals/slideover.vue'
import InlinePagination from './pagination/inline.vue'

new Vue({
    el: 'form',
    components: {
        FoldUnfold
    },
    directives: {
        check: checkstate
    }
})


new Vue({
    el: '.search-river',
    components: {
        Slideover
    },
})


new Vue({
    el: '.profile-detail',
    components: {
        InlinePagination
    }
})
