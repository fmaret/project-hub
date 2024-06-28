<template>
  <div class="dashboard">
    <div class="button" @click="showTicketModal = true; createTicket = true;">Créer ticket</div>
    <input type="text" v-model="filtersJson" @input="updateFiltersFromJson"/>
    <CardModal
    :isVisible="showTicketModal"
    :card="this.selectedCard"
    :createTicket = "createTicket"
    @close="showTicketModal = false; createTicket = false" 
    @card-updated="showTicketModal = false; getCards(); createTicket = false;"
    />
    <div>Liste des tickets</div>
    <table v-if="cards.cards">
      <thead>
        <tr>
          <th v-for="field, index in getCardsColumnsNames(cards)" :key="index">{{ field }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="card, cardIndex in cards.cards" :key="cardIndex">
          <th v-for="field, fieldIndex in getCardColumnsValues(card)" :key="fieldIndex">{{ field }}</th>
          <th>
            <div class="edit-button" @click="this.selectedCardIndex = cardIndex; showTicketModal = true">
              Editer
            </div>
          </th>
        </tr>
      </tbody>
    </table>
    <div class="page-selector">
      <div @click="if (currentCardPage > 1) currentCardPage--;getCards()">
        {{`<`}}
      </div>
      <div v-for="i in cards.pages" :key="i" :class="{'page-selected': i == currentCardPage}"
      @click="currentCardPage = i; getCards()">
        {{ i }}
      </div>
      <div @click="if (currentCardPage < cards.pages) currentCardPage++;getCards()">
        {{`>`}}
      </div>
    </div>
  </div>
</template>

<script>
import CardModal from "./CardModal.vue";
import { getCards, getProject } from "@/js/api.js"
export default {
  name: 'DashboardScreen',
  props: {
  },
  components: {
    CardModal
  },
  methods: {
    updateFiltersFromJson(event) {
        this.filtersJson = event.target.value;
        this.getCards();
    },
    async getCards() {
      this.cards = await getCards(this.projectId, this.currentCardPage, 10, this.filters);
    },
    getCardsColumnsNames(cards) {
      return ["Projet", "Id de la carte", "Type de la carte", ...Object.keys(cards.cards[0].fields), "Action"];
    },
    getCardColumnsValues(card) {
      return [card.projectName, card.cardId, card.cardTypeId, ...Object.values(card.fields).map(e=>{
        if (e.type == "LIST[MEMBER]" && e.value) return this.project.users.filter(f=>e.value.includes(f.id)).map(g=>g.username) ;
        else if (e.type == "MEMBER") return this.project.users.first(f=>f.id == e.value)
        return e.value;
      })]
    }
  },
  async mounted() {
    this.getCards();
    this.project = await getProject(this.projectId);
  },
  data: () => ({
    createTicket: false,
    showTicketModal: false,
    cards: [],
    projectId: 1,
    project: null,
    selectedCardIndex: null,
    currentCardPage: 1,
    filters: []
  }),
  computed: {
    selectedCard() {
      return this.selectedCardIndex != null ? this.cards.cards[this.selectedCardIndex] : null;
    },
    filtersJson: {
            get() {
              return JSON.stringify(this.filters, null, 2);  // Format JSON with indentation for readability
              
            },
            set(json) {
                try {
                    this.filters = JSON.parse(json);
                } catch (e) {
                  console.log("e", e);
                }
            }
        }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main-screen {
  background-color: grey;
}
.button {
  padding: 1rem;
  margin: 1rem;
  background-color: grey;
}

.edit-button {
  text-decoration: underline;
}

.edit-button:hover {
  cursor: pointer;
}

.button:hover {
  cursor: pointer;
}

.input-with-label > * {
  margin: 0.2rem;
}

.page-selector {
  display: flex;
}

.page-selector > * {
  padding:0.5rem;
}

.page-selector > *:hover {
  cursor: pointer;
}

.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.page-selected {
  text-decoration: underline;
  font-weight: bold;
}
</style>
