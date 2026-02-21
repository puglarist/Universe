using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

namespace Universe.AI
{
    public enum NpcReactionState { Neutral, Friendly, Hostile }

    [RequireComponent(typeof(NavMeshAgent))]
    public class NpcPatrolAndMemory : MonoBehaviour
    {
        public Transform[] patrolPoints;
        public NpcReactionState reactionState = NpcReactionState.Neutral;
        public List<string> memoryLog = new List<string>();

        private NavMeshAgent agent;
        private int index;

        private void Awake() => agent = GetComponent<NavMeshAgent>();

        private void Start()
        {
            if (patrolPoints.Length > 0)
                agent.SetDestination(patrolPoints[0].position);
        }

        private void Update()
        {
            if (patrolPoints.Length == 0 || agent.pathPending) return;
            if (agent.remainingDistance > 0.5f) return;

            index = (index + 1) % patrolPoints.Length;
            agent.SetDestination(patrolPoints[index].position);
        }

        public void RememberPlayerAction(string action)
        {
            memoryLog.Add($"{System.DateTime.UtcNow:o} :: {action}");
        }
    }
}
