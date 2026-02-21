using UnityEngine;

namespace Universe.Economy
{
    public class EconomyStarter : MonoBehaviour
    {
        public int money;
        public int scrapCount;

        public void CollectScrap(int amount = 1) => scrapCount += amount;

        public void SellScrap(int unitPrice = 2)
        {
            money += scrapCount * unitPrice;
            scrapCount = 0;
        }

        public bool BuyItem(int cost)
        {
            if (money < cost) return false;
            money -= cost;
            return true;
        }
    }
}
