import { categoryMap } from './CategoryMap';

class TrieNode {
    constructor() {
        this.children = {};
        this.isWord = false;
        this.code = "";
    }
}

export default class CategoryTree {
    constructor() {
        this.categories = {}
        for (const [country, categories] of categoryMap) {
            if (!this.categories[country]) {
                this.categories[country] = new TrieNode()
            }
            for (const [name, code] of categories) {
                let node = this.categories[country];
                for (let i = 0; i < name.length; i++) {
                    let char = name[i].toLowerCase();
                    if (!node.children[char]) {
                        node.children[char] = new TrieNode();
                    }
                    node = node.children[char];
                }
                node.code = code;
                node.isWord = true;
            }
        }
    }

    beginsWith(country, prefix) {
        if (!this.categories[country]) {
            return []
        }
        let matches = []
        let cur = this.categories[country]

        for (let i = 0; i < prefix.length; i++) {
            let char = prefix[i].toLowerCase();
            if (!cur.children[char]) {
                return [];
            }
            cur = cur.children[char];
        }

        const queue = [["", cur]];
        while (queue.length > 0) {
            const [suffix, node] = queue.shift()
            if(node.isWord) {
                const word = (prefix+suffix).toLowerCase()
                matches.push({
                    name: word.charAt(0).toUpperCase() + word.slice(1),
                    code: node.code
                })
            }
            for (const char in node.children) {
                queue.push([suffix+char, node.children[char]])
            }

        }
        return matches;
    }
}

