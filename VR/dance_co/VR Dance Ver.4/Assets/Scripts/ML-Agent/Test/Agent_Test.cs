using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class Agent_Test : Agent
{
    public Transform pivot, target;

    public float moveSpeed = 1f;

    int select = -1;

    CorWrong cw;

    void Awake()
    {
        Monitor.SetActive(true);
        StartCoroutine(timeChecker());
        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();
    }

    void ResetTarget()
    {
        Vector3 targetRandomPos = new Vector3(Random.Range(-1.5f, 1.5f), Random.Range(1.4f, 2.0f), Random.Range(-1f, 1f));
        target.transform.position = targetRandomPos + pivot.position;
    }

    public override void AgentReset()
    {
        ResetTarget();
    }

    public override void CollectObservations()
    {
        AddVectorObs(target.transform.position.y);
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        if (select == 0)
        {
            if (target.position.y >= 1.65f)
            {
                cw.correct += 1;
                AddReward(1f);
            }

            else
            {
                cw.wrong += 1;
                AddReward(-1f);
            }
        }

        else if(select == 1)
        {
            if (target.position.y >= 1.65f)
            {
                cw.wrong += 1;
                AddReward(-1f);
            }

            else
            {
                cw.correct += 1;
                AddReward(1f);
            }
        }

        ResetTarget();
    }

    IEnumerator timeChecker()
    {
        while(true)
        {
            yield return new WaitForSeconds(100f);

            cw.change = true;
            Done();
        }
    }
}
