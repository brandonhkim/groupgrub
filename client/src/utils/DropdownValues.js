class DropdownValues {
    constructor(obj) {
        this.value = obj.value;
        this.handler = (val) => {
            obj.handler(val);
        }
        this.heading = obj.heading;
        this.prefix = obj.prefix;
        this.minRange = obj.minRange;
        this.maxRange = obj.maxRange;
        this.incVal = obj.incVal;
    }
}

export const getDropdownValues = (numResults, setNumResults, priceRange, setPriceRange, driveRadius, setDriveRadius) => [
    new DropdownValues({ 
        value: numResults,
        handler: setNumResults,
        heading: "Number of restaurant options",
        prefix: "number",
        minRange: 10,
        maxRange: 30,
        incVal: 10
    }),
    new DropdownValues({
        value: priceRange,
        handler: setPriceRange,
        heading: "Maximum price range",
        prefix: "price",
        minRange: 1,
        maxRange: 4,
        incVal: 1
    }),
    new DropdownValues({
        value: driveRadius,
        handler: setDriveRadius,
        heading: "Maximum driving radius",
        prefix: "radius",
        minRange: 5,
        maxRange: 25,
        incVal: 5
    }),
];