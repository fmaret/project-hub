<template>
  <div class="edition">
    <CardModal></CardModal>
  </div>
</template>

<script>
import CardModal from "./CardModal.vue";
import { getCards, getProject } from "@/js/api.js"
export default {
  name: 'EditionScreen',
  props: {
  },
  components: {
    CardModal
  },
  methods: {
    async getCards() {
      this.cards = await getCards(this.projectId);
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
