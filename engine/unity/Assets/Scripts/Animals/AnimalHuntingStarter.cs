using UnityEngine;

namespace Universe.Animals
{
    public class AnimalHuntingStarter : MonoBehaviour
    {
        public GameObject deerPrefab;
        public GameObject footprintPrefab;

        public void SpawnDeer(Vector3 position)
        {
            if (deerPrefab != null)
                Instantiate(deerPrefab, position, Quaternion.identity);
        }

        public void DropFootprint(Vector3 position)
        {
            if (footprintPrefab != null)
                Instantiate(footprintPrefab, position, Quaternion.identity);
        }
    }
}
