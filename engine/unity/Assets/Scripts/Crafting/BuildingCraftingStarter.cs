using UnityEngine;

namespace Universe.Crafting
{
    public class BuildingCraftingStarter : MonoBehaviour
    {
        public GameObject woodenWallPrefab;
        public GameObject doorPrefab;
        public GameObject workbenchPrefab;

        public void PlaceAtCursor(GameObject prefab)
        {
            if (prefab == null) return;
            if (!Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out RaycastHit hit, 100f)) return;
            Instantiate(prefab, hit.point, Quaternion.identity);
        }
    }
}
