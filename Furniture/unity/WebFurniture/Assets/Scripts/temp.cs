using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class temp : MonoBehaviour
{
    public Transform target = null;
    private Transform makeTarget = null;
    private management Manager;

    private void Start()
    {
        Manager = GameObject.Find("Manager").GetComponent<management>();
    }

    private void Update()
    {
        if(Input.GetMouseButton(0) && makeTarget != null)
        {
            var point = Camera.main.ScreenToWorldPoint(new Vector3(Input.mousePosition.x, Input.mousePosition.y, -Camera.main.transform.position.z));
            point.y = 0.5f;

            makeTarget.position = point;
            makeTarget.GetComponent<toTransparent>().toTransparentMaterial();
        }

        if (Input.GetMouseButtonUp(0) && makeTarget != null)
        {
            if (Input.mousePosition.x >= 1460)
            {
                Destroy(makeTarget.gameObject);
                makeTarget = null;
            }

            var pos = Manager.selectCell.transform.position;
            makeTarget.position = new Vector3(pos.x + 0.5f, pos.y + 0.5f, pos.z - 0.5f);
            makeTarget.GetComponent<toTransparent>().toBaseMaterial();
            makeTarget = null;
        }
    }

    public void ClickFurniture()
    {
        var point = Camera.main.ScreenToWorldPoint(new Vector3(Input.mousePosition.x, Input.mousePosition.y, -Camera.main.transform.position.z));
        point.y = 0.5f;

        makeTarget = Instantiate(target);
        makeTarget.position = point;
    }
}
