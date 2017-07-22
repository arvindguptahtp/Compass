module.exports = {
    has_props (obj) { return Object.keys(obj).length > 0 && obj.constructor === Object },
    
    is_empty (obj) { return Object.keys(obj).length === 0 && obj.constructor === Object },
    
    is_object (item) { return (item && typeof item === 'object' && !Array.isArray(item) && item !== null) },
}
