using UnityEngine;

namespace Universe.AI
{
    public class WorldGenerationStarter : MonoBehaviour
    {
        public Light sun;
        public float dayNightCycleSpeed = 10f;

        private void Update()
        {
            if (sun != null)
                sun.transform.Rotate(Vector3.right, dayNightCycleSpeed * Time.deltaTime);
        }

        public void GenerateProceduralTerrain() => Debug.Log("Procedural terrain generation placeholder.");
        public void PlaceRandomBuildings() => Debug.Log("Random building placement placeholder.");
        public void SetWeather(string weatherType) => Debug.Log($"Weather set: {weatherType}");
    }
}
