export default {
    name: 'inplace-pagination',
    data () {
        return {
            page: 1,
            item_limit: 4,
            items: [],
            current_items: [],
        }
    },
    computed: {
        pages () {
            return Math.ceil(this.items.length / this.item_limit)
        },
        lower_range () {
            if (this.page == 1) {
                return 0
            } else {
                return (this.page - 1) * this.item_limit
            }
        },
        upper_range () {
            return this.lower_range + this.item_limit
        },
        has_prev () {
            return (this.page > 1)
        },
        has_next () {
            return (this.page < this.pages)
        }
    },
    methods: {
        toggle_items(items, viz) {
            items.forEach(
                (item) => {
                    item.elm.style.display = viz
                }
            )
        },
        
        show_page(page_num) {
            this.page = page_num
            this.toggle_items(this.current_items, "none")
            this.current_items = this.items.slice(this.lower_range, this.upper_range)
            this.toggle_items(this.current_items, "flex")
        },
        
        prev_page () {
            (this.has_prev) ? this.show_page(this.page - 1) : false
        },

        next_page () {
            (this.has_next) ? this.show_page(this.page + 1) : false
        }
    },
    mounted () {
        // get the items to paginate, remove textnode/whitespace
        this.items = this.$slots.bd[0].children.filter( 
            (item) => {
                if (item.tag) {
                    item.elm.style.display = "none"
                    return item
                }
            }
        )
       
        this.show_page(1)
    }
}
