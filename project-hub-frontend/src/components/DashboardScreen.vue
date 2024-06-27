<template>
  <div class="dashboard">
    <div class="button" @click="showTicketModal = true; createTicket = true;">Créer ticket</div>
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
    <div>
      <div @click="if (currentCardPage > 1) currentCardPage--;getCards()">
        précédent
      </div>
      <div @click="if (currentCardPage < cards.pages) currentCardPage++;getCards()">
        suivant
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
    async getCards() {
      this.cards = await getCards(this.projectId, this.currentCardPage, 10);
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
  }),
  computed: {
    selectedCard() {
      return this.selectedCardIndex != null ? this.cards.cards[this.selectedCardIndex] : null;
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
</style>
