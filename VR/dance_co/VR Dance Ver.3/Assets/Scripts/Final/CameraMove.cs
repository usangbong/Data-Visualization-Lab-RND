using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMove : MonoBehaviour
{
    public GameObject character;
    public List<bool> leftList = new List<bool>();
    public List<bool> rightList = new List<bool>();

    void Start()
    {
        for(int i=0;i<6;i++)
        {
            leftList.Add(false);
            rightList.Add(false);
        }
    }

    void Update()
    {
        if(leftList[0] && rightList[0])
        {
            character.transform.Translate(Vector3.forward * 1f * Time.deltaTime);
        }

        else if(leftList[1] && rightList[1])
        {
            character.transform.Translate(Vector3.back * 1f * Time.deltaTime);
        }

        else if(leftList[2] && rightList[2])
        {
            character.transform.Translate(Vector3.left * 1f * Time.deltaTime);
        }

        else if(leftList[3] && rightList[3])
        {
            character.transform.Translate(Vector3.right * 1f * Time.deltaTime);
        }

        else if(leftList[4] && rightList[4])
        {
            character.transform.Translate(Vector3.up * 1f * Time.deltaTime);
        }

        else if(leftList[5] && rightList[5])
        {
            character.transform.Translate(Vector3.down * 1f * Time.deltaTime);
        }
    }
}
