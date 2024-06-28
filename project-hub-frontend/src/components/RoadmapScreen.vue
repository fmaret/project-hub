<template>
  <div class="roadmap">
    {{ orderedCards }}
    <div class="header-container">
      <div class="header">
        <div v-for="(column, index) in columns" :key="index" class="header-item">{{ column }}</div>
      </div>
    </div>
    <div class="body-container">
      <div class="card-line" v-for="card, index in displayedCards" :key="card.cardId">
        <div v-for="cardPart in orderedCards" class="card" :style="{'left': `${150*cardPart.column}px`, 'top': `${25*cardPart.line}px`, 'width': `${150*cardPart.width}px`}">
          Ticket {{ cardPart.id }}
        </div>
    </div>
    </div>
    
  </div>
</template>

<script>
export default {
  data() {
    return {
      columns: ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12"],
      cards: {
  "cards": [
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 1,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": "Coucou",
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": "[]",
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": ['2024-01', '2024-02'],
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 2,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": "[]",
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": ['2024-01'],
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 3,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": "[]",
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": ['2024-02'],
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 4,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": "[]",
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": ['2024-04'],
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 5,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 6,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 7,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 8,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 9,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 10,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": "test",
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": "[1]",
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 11,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 12,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 13,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 14,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 15,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    },
    {
      "projectName": 1,
      "projectId": 1,
      "cardId": 16,
      "cardTypeId": 1,
      "fields": {
        "title": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "description": {
          "value": null,
          "type": "STRING",
          "values": {}
        },
        "assignees": {
          "value": null,
          "type": "LIST[MEMBER]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        },
        "sprint": {
          "value": null,
          "type": "LIST[ENUM_8]",
          "values": {
            "8": [
              "2024-01",
              "2024-02",
              "2024-03",
              "2024-04",
              "2024-05",
              "2024-06",
              "2024-07",
              "2024-08",
              "2024-09",
              "2024-10",
              "2024-11",
              "2024-12"
            ]
          }
        }
      }
    }
  ],
  "itemsPerPage": 100,
  "page": 1,
  "pages": 1
}
    };
  },
  methods: {
    mergeAdjacentElements(elements) {
      // Regrouper les éléments par ligne
      const lines = elements.reduce((acc, elem) => {
        if (!acc[elem.line]) {
          acc[elem.line] = [];
        }
        acc[elem.line].push(elem);
        return acc;
      }, {});

      // Fonction pour fusionner les éléments adjacents dans une ligne avec le même id
      const mergeLine = (line) => {
        line.sort((a, b) => a.column - b.column);
        const merged = [];
        let current = line[0];

        for (let i = 1; i < line.length; i++) {
          const next = line[i];
          if (current.column + current.width === next.column && current.id === next.id) {
            // Si les éléments sont adjacents et ont le même id, augmenter la largeur du courant
            current.width += next.width;
          } else {
            // Sinon, ajouter l'élément courant à la liste fusionnée et passer au suivant
            merged.push(current);
            current = next;
          }
        }
        merged.push(current); // Ajouter le dernier élément traité

        return merged;
      };

      // Fusionner les éléments pour chaque ligne
      const mergedLines = Object.keys(lines).map(line => mergeLine(lines[line]));

      // Fusionner toutes les lignes fusionnées en une seule liste
      return mergedLines.flat();
    },
  },
  computed: {
    displayedCards() {
      return this.cards.cards.filter(card => card.fields.sprint.value);
    },
    orderedCards() {
      let obj = [];
      let columnsLines = new Array(this.columns.length).fill(0);
      this.displayedCards.map(card => {
        let columnsIds = card.fields.sprint.value.map(sprint => (this.columns.indexOf(sprint)));
        columnsIds.map(columnId => {
          let line = columnsLines[columnId]++;
          let column = columnId;
          obj.push({
          "title": card.title,
          "line": line,
          "column": column,
          "width": 1,
          "id": card.cardId
          });
        })
      });
      // merge elements
      return this.mergeAdjacentElements(obj);

    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.roadmap {
  overflow-x: auto;
  white-space: nowrap;
}

.body-container {
  position:relative;
}

.header {
  display: flex;
}

.header-item {
  min-width: 150px; /* Ajustez cette valeur selon vos besoins */
  padding: 10px;
  border: 1px solid #ddd;
  box-sizing: border-box;
  flex-shrink: 0; /* Empêche les colonnes de se rétrécir */
}

.card {
  border: 1px solid black;
  background-color: darkgreen;
  color: white;
  /* padding: 1rem 0; */
  position: absolute;
}

.card-line {
  display: flex;
}

</style>